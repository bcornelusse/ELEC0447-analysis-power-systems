/**
 * =========================================================================
 * ELEC0447: Analysis of Electric Power and Energy Systems (ULiège)
 * Unified Google Apps Script Webhook for Interactive Course Quizzes
 * =========================================================================
 * 
 * This single Google Apps Script serves as the unified receiver for all
 * interactive quizzes in ELEC0447 (Transmission Lines, Power Flow, Transformers, etc.).
 * 
 * Setup Instructions (takes ~2 minutes):
 * -------------------------------------
 * 1. Open Google Sheets (https://sheets.google.com) and create a new spreadsheet,
 *    e.g. named "ELEC0447 - Quiz Submissions".
 * 2. In the top menu, go to: Extensions > Apps Script.
 * 3. Delete any boilerplate code in the script editor and paste this entire file.
 * 4. Click the blue "Deploy" button (top-right) -> "New deployment".
 * 5. Under "Select type" (gear icon), select "Web app".
 * 6. Set the configuration options:
 *    - Description: "ELEC0447 Quiz Responses Webhook"
 *    - Execute as: "Me" (your Google account)
 *    - Who has access: "Anyone" (crucial so students can submit without Google login prompts)
 * 7. Click "Deploy", review/grant permissions when prompted.
 * 8. Copy the generated Web App URL (starts with https://script.google.com/macros/s/.../exec).
 * 9. Paste that URL into the `GOOGLE_SCRIPT_URL` variable in your quiz HTML files:
 *    - Lectures/TransmissionLine/quiz_transmission_lines.html
 *    - Lectures/IntroPowerFlow/quiz_power_flow.html
 *    - Lectures/TransfomerAndPF/quiz_transformers.html
 * 
 * How Submissions are Stored in Your Spreadsheet:
 * -----------------------------------------------
 * - A master tab "All_Submissions" records every attempt across all course quizzes.
 * - Individual tabs (e.g. "Transmission Lines", "Power Flow", "Transformers")
 *   are automatically created for each quiz, containing the student's score,
 *   percentage, question-by-question breakdown, and raw JSON payload.
 */

function doPost(e) {
  try {
    var contents = e.postData.contents;
    var data = JSON.parse(contents);
    
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    
    var timestamp = data.timestamp || new Date().toISOString();
    var course = data.course || "ELEC0447";
    var quizId = data.quiz_id || "general";
    var quizTitle = data.quiz_title || "Course Quiz";
    var studentName = (data.name || "Anonymous").trim();
    var studentEmail = (data.email || "N/A").trim();
    var score = Number(data.score) || 0;
    var total = Number(data.total) || 0;
    var percentage = (data.percentage !== undefined) ? data.percentage + "%" : Math.round((score / total) * 100) + "%";
    
    // -------------------------------------------------------------------------
    // 1. Log to Master Tab ("All_Submissions")
    // -------------------------------------------------------------------------
    var masterSheet = ss.getSheetByName("All_Submissions");
    if (!masterSheet) {
      masterSheet = ss.insertSheet("All_Submissions", 0);
      masterSheet.appendRow([
        "Timestamp", "Course", "Quiz ID", "Quiz Title", 
        "Student Name", "Student Email", "Score", "Total", "Percentage"
      ]);
      masterSheet.getRange(1, 1, 1, 9)
        .setFontWeight("bold")
        .setBackground("#00843B")
        .setFontColor("#FFFFFF");
      masterSheet.setFrozenRows(1);
    }
    masterSheet.appendRow([
      timestamp, course, quizId, quizTitle, 
      studentName, studentEmail, score, total, percentage
    ]);
    
    // -------------------------------------------------------------------------
    // 2. Log to Quiz-Specific Tab (named after quiz_title, truncated to 30 chars)
    // -------------------------------------------------------------------------
    var tabName = (quizTitle.replace(/[^a-zA-Z0-9_\- ]/g, "").substring(0, 30)).trim() || "Quiz_Details";
    var quizSheet = ss.getSheetByName(tabName);
    if (!quizSheet) {
      quizSheet = ss.insertSheet(tabName);
      quizSheet.appendRow([
        "Timestamp", "Student Name", "Student Email", 
        "Score", "Total", "Percentage", "Summary Breakdown", "Answers JSON"
      ]);
      quizSheet.getRange(1, 1, 1, 8)
        .setFontWeight("bold")
        .setBackground("#00632B")
        .setFontColor("#FFFFFF");
      quizSheet.setFrozenRows(1);
    }
    
    // Format compact question breakdown: "Q01: ✓; Q02: ✗; Q03: ✓..."
    var summaryBreakdown = "";
    if (Array.isArray(data.answers)) {
      summaryBreakdown = data.answers.map(function(item) {
        var qId = item.id || ("Q" + item.question_index);
        return qId + ": " + (item.is_correct ? "✓" : "✗");
      }).join("; ");
    }
    
    quizSheet.appendRow([
      timestamp, studentName, studentEmail, 
      score, total, percentage, summaryBreakdown, JSON.stringify(data.answers || [])
    ]);
    
    return ContentService.createTextOutput(JSON.stringify({
      result: "success",
      message: "Submission successfully logged for " + studentName + " (" + quizTitle + ")"
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      result: "error",
      error: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: "active",
    course: "ELEC0447 - Analysis of Electric Power and Energy Systems",
    message: "Google Apps Script webhook is online and ready to accept quiz submissions."
  })).setMimeType(ContentService.MimeType.JSON);
}
