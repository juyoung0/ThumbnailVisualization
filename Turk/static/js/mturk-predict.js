 var num = $('#tn').val();
 // SHOULD 180
 var CLOCK = 180;
 var clock=CLOCK;

 function show_article(){
    document.getElementById("finish-read").disabled = true;
     $('#article_instruction').css("display", "none");
     $('#show_article').css("display", "block");
     $('#article-1').css("display", "block");

    clock=CLOCK;
    var timer = setInterval(function() {
      clock--;
      $('#timeLeft').html("Time Left : " + clock);
      if(clock<=0) {
        clearInterval(timer);
        hide_article();
      }
      if(clock<=60) { // 120초 경과후부터는 넘길 수 있음
        document.getElementById("finish-read").disabled = false;
      }
    }, 1000);
  }

  function allChecked1(){
    if($("#ques1").val().length>70 && $("#ques2").val().length>70 && $("#ques3").val().length>70)
      return true;
    else
      return false;
  }
   function allChecked2(){
    if($("#ques4").val().length>70 && $("#ques5").val().length>70 && $("#ques6").val().length>70 && $("#ques7").val().length>70)
      return true;
    else
      return false;
  }

  function hide_article(){
    $('#task_article').css("display", "none");
    $('#timeLeft').html("Time is done");
    $('#attention_check').css("display", "block");

    $('#valid-row1').css("display", "block");
    //$('#valid-row2').css("display", "block");
    checkValid();
  }


$("#btn-start-prediction").click(function(){
    $('#prediction_instruction').css("display", "none");
    $('#show_thumbnail').css("display", "block");
    $("#helpful-chk1").css("display", "block");
    if (num == 1) {
        $('.thumbnail-1').css("display", "block");        }
    else if (num == 2) {
        $('.thumbnail-2').css("display", "block");     }
    else if (num == 3) {
        $('.thumbnail-3').css("display", "block");     }
    else if (num == 4) {
        $('.thumbnail-4').css("display", "block");     }
    else if (num == 5) {
        $('.thumbnail-5').css("display", "block");     }
    else if (num == 6) {
        $('.thumbnail-6').css("display", "block");     }
    else if (num == 7) {
        $('.thumbnail-7').css("display", "block");     }
    else if (num == 8) {
        $('.thumbnail-8').css("display", "block");     }
});

$("#btn-task-description").click(function() {

    if(help1!=0){
        $("#helpful-chk1").css("display", "none");
        $("#get-description").css("display", "block");
        $("#help1").val(help1);
     }else
        alert('Please submit answer');

})

$("#btn-task-article").click(function() {
    if($("#description").val().length > 70){
        $('#task_prediction').css("display", "none");
        $("#task_article").css("display", "block");
        $("#article_instruction").css("display", "block");
        $("#show_description").val($("#description").val());
        $('#des').val($("#description").val());
        //$('#ques7').val($("#description").val());
    }else
        alert('Please write down more than 70 characters');

});

$("#btn-show-article").click(function() {
    show_article();
});

$("#finish-read").click(function() {
     $('#task_article').css("display", "none");
     $('#attention_check').css("display", "block");
     $('#valid-row1').css("display", "block");
});


var trap1 = 0, trap2 = 0;
var help1 = 0, help2 = 0, help3=0;

$('#trapbtn1 button').click(function() {
  $(this).addClass('active').siblings().removeClass('active');
  trap1 = $(this).text();
});

$('#trapbtn2 button').click(function() {
  $(this).addClass('active').siblings().removeClass('active');
  trap2 = $(this).text();
});

$('#help-btn1 button').click(function() {
  $(this).addClass('active').siblings().removeClass('active');
  help1 = $(this).text();
});

$('#help-btn2 button').click(function() {
  $(this).addClass('active').siblings().removeClass('active');
  help2 = $(this).text();
});

$('#help-btn3 button').click(function() {
  $(this).addClass('active').siblings().removeClass('active');
  help3 = $(this).text();
});

$("#trap-ans1").click(function() {
    if(trap1!=""){
          $('#valid').val(trap1);

          // wrong answer -> fail!
         if(trap1!="Immigration"){
                $('#passTrap').val(false);
                $( "#ans-form" ).submit();
          }
          else{
            $('#attention_check').css("display", "none");
            $('#modification-instruction').css("display", "block");
          }
     }else{
           alert('Please submit answer');
     }
});
$("#trap-ans2").click(function() {
    if(trap2!=""){
          $('#valid').val(trap2);

          // wrong answer -> fail!
         if(trap2!="Internet rate"){
                $('#passTrap').val(false);
                $( "#ans-form" ).submit();
          }
         $('#attention_check').css("display", "none");
         $('#modification-instruction').css("display", "block");
     }else{
         alert('Please submit answer');
     }
});


$("#btn-show-modification").click(function() {
     $('#modification-instruction').css("display", "none");
     $('.container').css("display", "none");
     $('.container-fluid').css("display", "block");
     $('#show-modification').css("display", "block");
     $('#helpful-chk2').css("display", "block");
        $('#m-article-1').css("display", "block");
        if (num==1) {
            $('#m-thumbnail-1').css("display", "block");
           // $('#tn').val("1");
            }
        else if (num==2) {
            $('#m-thumbnail-2').css("display", "block");
           // $('#tn').val("2");
         }
        else if (num==3) {
            $('#m-thumbnail-3').css("display", "block");
           // $('#tn').val("3");
        }
        else if (num==4) {
            $('#m-thumbnail-4').css("display", "block");
           // $('#tn').val("4");
        }
        else if (num==5) {
            $('#m-thumbnail-5').css("display", "block");
           // $('#tn').val("5");
        }
        else if (num==6) {
            $('#m-thumbnail-6').css("display", "block");
           // $('#tn=').val("6");
        }
        else if (num==7) {
            $('#m-thumbnail-7').css("display", "block");
           // $('#tn=').val("7");
        }
        else if (num==8) {
            $('#m-thumbnail-8').css("display", "block");
          //  $('#tn=').val("8");
          }
});

$("#btn-task-modification").click(function() {
    if(help2!=0){
        $('#helpful-chk2').css("display", "none");
        $('#modification').css("display", "block");
        $('#questions_tn').css("display", "block");
        $("#help2").val(help2)
    }else
        alert('Please submit answer');
});

$("#btn-task-final").click(function() {
    if(help3!=0){
        $('#show-modification').css("display", "none");
        $("#help3").val(help3);
        $("#final-div").css("display", "block");
    }else
        alert('Please submit answer');
});

$("#next_questions").click(function() {
    if(allChecked1()) {
         $("#q1").val($("#ques1").val());
         $("#q2").val($("#ques2").val());
         $("#q3").val($("#ques3").val());
        $('#questions_tn').css("display", "none");
        $('#questions_d').css("display", "block");
    } else
        alert('Please write down all answers more than 70 characters');
});



$("#submit_modified").click(function() {
    if(allChecked2()){
         $("#q4").val($("#ques4").val());
         $("#q5").val($("#ques5").val());
         $("#q6").val($("#ques6").val());
         $("#q7").val($("#ques7").val());
        $('#modification').css("display", "none");
        $('.container-fluid').css("display", "block");
        $("#helpful-chk3").css("display", "block");
    }else
        alert('Please write down all answers more than 70 characters');
});



$("#description").keyup(function(e) {
    var content = $(this).val();
   $('#counter').html("("+content.length+" / 300 characters)");
   $(this).val(content.substring(0, 300));
});
$("#ques1").keyup(function (e) {
    var content = $(this).val();
   $('#counter1').html("("+content.length+" / 150 characters)");
   $(this).val(content.substring(0, 150));
});
$("#ques2").keyup(function (e) {
    var content = $(this).val();
   $('#counter2').html("("+content.length+" / 150 characters)");
   $(this).val(content.substring(0, 150));
});
$("#ques3").keyup(function (e) {
    var content = $(this).val();
   $('#counter3').html("("+content.length+" / 150 characters)");
   $(this).val(content.substring(0, 150));
});
$("#ques4").keyup(function (e) {
    var content = $(this).val();
   $('#counter4').html("("+content.length+" / 150 characters)");
   $(this).val(content.substring(0, 150));
});
$("#ques5").keyup(function (e) {
    var content = $(this).val();
   $('#counter5').html("("+content.length+" / 150 characters)");
   $(this).val(content.substring(0, 150));
});
$("#ques6").keyup(function (e) {
    var content = $(this).val();
   $('#counter6').html("("+content.length+" / 150 characters)");
   $(this).val(content.substring(0, 150));
});
$("#ques7").keyup(function (e) {
    var content = $(this).val();
   $('#counter7').html("("+content.length+" / 300 characters)");
   $(this).val(content.substring(0, 300));
});