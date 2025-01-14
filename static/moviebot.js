let question = 1;
let query = "";

function getBotResponse() {
  var rawText = $("#textInput").val();
  var userHtml = `<div class="user-message">${rawText}</div>`;
  $("#chatbox").append(userHtml);
  $("#textInput").val('');

  if (question === 1) {
    question++;
    query += rawText.toLowerCase();
    setTimeout(function () {
      $('#chatbox').append('<div class="bot-message">Great! Now, could you share your favorite actor or actress?</div>');
    }, 500);
  } else if (question === 2) {
    question++;
    query += ' ' + rawText.toLowerCase();
    setTimeout(function () {
      $('#chatbox').append('<div class="bot-message">Nice! Finally, can you tell me the type of movie you prefer? (e.g., action, comedy, etc.)</div>');
    }, 500);
  } else {
    question = 1; // Reset after all questions
    query += ' ' + rawText.toLowerCase();
    setTimeout(function () {
      $('#chatbox').append('<div class="bot-message">Fetching movie recommendations based on your preferences...</div>');

      // Send the query to Flask back-end for recommendations
      $.post("/moviebot/recommend", { msg: query }, function (data) {
        if (data.movies) {
          data.movies.forEach(function (movie) {
            $('#chatbox').append(`<div class="bot-message">${movie.title}</div>`);
          });
        }
      });
    }, 500);
  }

  $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight); // Auto-scroll to the bottom
}

$("#sendBtn").click(function() {
  if ($("#textInput").val()) {
    getBotResponse();
  }
});

$("#textInput").keypress(function (e) {
  if (e.which == 13 && $("#textInput").val().length > 0) {
    getBotResponse();
  }
});

