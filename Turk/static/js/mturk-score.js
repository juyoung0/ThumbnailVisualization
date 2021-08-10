var CLOCK = 180;
var clock=CLOCK;
var num = 1;
var descriptions=[];
var des_size = 5;
var des_idx = 0;

  function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
  }

for(var i=0; i<des_size; ++i){
    descriptions[i] = i+1;
}
shuffleArray(descriptions);
console.log(descriptions)

//Thumbnail 답변 체크
function allChecked1(){
if(ques1!=0 && ques2!=0 && ques3!=0 && ques4!=0 && ques5!=0)
  return true;
else
  return false;
}

function allChecked2(){
if(ques6!=0 && ques7!=0 && ques8!=0 && non!=0)
  return true;
else
  return false;
}

$("#btn-show-article").click(function() {
    num = Number($("#tn-num").val());
    $("#tn").val(num);
    show_article();
});

$("#finish-read").click(function() {
    $('#task-article').css("display", "none");
    $("#attention-check").css("display", "block");
    $("#valid-row1").css("display", "block");
});

function hide_article(){
    $('#task-article').css("display", "none");
    $('#timeLeft').html("Time is done");
    $('#attention-check').css("display", "block");

    $('#valid-row1').css("display", "block");
    //$('#valid-row2').css("display", "block");
    checkValid();
  }


var trap1 = 0, trap2 = 0;

$('#trapbtn1 button').click(function() {
  $(this).addClass('active').siblings().removeClass('active');
  trap1 = $(this).text();
});

$('#trapbtn2 button').click(function() {
  $(this).addClass('active').siblings().removeClass('active');
  trap2 = $(this).text();
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
            $('.container').css("display", "none");
            $('.container-fluid').css("display", "block");
            $("#task-scoring").css("display", "block");
            $("#score-instruction2").css("display", "block");
          }
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
        $('.container').css("display", "none");
        $('.container-fluid').css("display", "block");
        $("#task-scoring").css("display", "block");
        $("#score-instruction2").css("display", "block");
     }
});

var ques6=0, ques7=0, ques8=0;
var non=0;



$('#button-6 button').click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    ques6 = $(this).text();
});
$('#button-7 button').click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    ques7 = $(this).text();
});
$('#button-8 button').click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    ques8 = $(this).text();
});
$("#button-non-1 button").click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    non = $(this).text();
});
$("#button-non-2 button").click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    non = $(this).text();
});
$("#button-non-3 button").click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    non = $(this).text();
});
$("#button-non-4 button").click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    non = $(this).text();
});
$("#button-non-5 button").click(function() {
    $(this).addClass('active').siblings().removeClass('active');
    non = $(this).text();
});


$("#btn-start-scoring2").click(function() {
    $("#score-instruction2").css("display", "none");
    $("#show-d-questions").css("display", "block");
    $("#d-article-1").css("display", "block");
    if (num == 1) { $('#d-thumbnail-1').css("display", "block"); }
    else if (num == 2) { $('#d-thumbnail-2').css("display", "block"); }
    else if (num == 3) { $('#d-thumbnail-3').css("display", "block"); }
    else if (num == 4) { $('#d-thumbnail-4').css("display", "block"); }
    else if (num == 5) { $('#d-thumbnail-5').css("display", "block"); }
    else if (num == 6) { $('#d-thumbnail-6').css("display", "block"); }
    else if (num == 7) { $('#d-thumbnail-7').css("display", "block"); }
    else if (num == 8) { $('#d-thumbnail-8').css("display", "block"); }
    $("#description-id").html("Description (" + Number(Number(des_idx)+1)+ " / 5)");
    $("#description-"+descriptions[des_idx]).css("display", "block");
    $("#nonsense-"+ Number(Number(des_idx)+1)).css("display", "block");
    console.log(des_idx)
});

$("#btn-task-finish").click(function() {
    if(allChecked2()){
         $("#d"+descriptions[des_idx]+"q1").val(ques6);
         $("#d"+descriptions[des_idx]+"q2").val(ques7);
         $("#d"+descriptions[des_idx]+"q3").val(ques8);
         $("#checkval"+ Number(Number(des_idx)+1)).val(non);
         ques6 = 0
         ques7 = 0
         ques8 = 0
         non = 0
         $('button').removeClass('active');

        //finish task
        if(des_idx==des_size-1){

             if (des_idx+1 == 5 && $("#checkval"+ Number(Number(des_idx)+1)).val() != 5) {
                $('#passTrap').val(false);
                $( "#ans-form" ).submit();
            }
            $("#task-scoring").css("display", "none");
            $('#final-div').css("display", "block");
        }else{
            $("#description-"+descriptions[des_idx]).css("display", "none");
            $("#nonsense-"+ Number(Number(des_idx)+1)).css("display", "none");
            if (des_idx + 1 ==1 && $("#checkval"+ Number(Number(des_idx)+1)).val() != 4) {
                $('#passTrap').val(false);
                console.log("check1");
                $( "#ans-form" ).submit();
            }
            else if (des_idx+1 == 2 && $("#checkval"+ Number(Number(des_idx)+1)).val() != 2) {
                $('#passTrap').val(false);
                $( "#ans-form" ).submit();
            }
            else if (des_idx+1 == 3 && $("#checkval"+ Number(Number(des_idx)+1)).val() != 6) {
                $('#passTrap').val(false);
                $( "#ans-form" ).submit();
            }
            else if (des_idx+1 == 4 && $("#checkval"+ Number(Number(des_idx)+1)).val() != 2) {
                $('#passTrap').val(false);
                $( "#ans-form" ).submit();
            }
            des_idx++;
            $("#description-id").html("Description (" + Number(Number(des_idx)+1)+" / 5)");
            $("#description-"+descriptions[des_idx]).css("display", "block");
            $("#nonsense-"+ Number(Number(des_idx)+1)).css("display", "block");

        }
    }else{
      alert('Please submit ratings for each statement');
    }
});

function show_article(){
document.getElementById("finish-read").disabled = true;
 $('#article-instruction').css("display", "none");
 $('#show-article').css("display", "block");
 $('#article-1').css("display", "block");

clock=CLOCK;
var timer = setInterval(function() {
  clock--;
  $('#timeLeft').html("Time Left : " + clock);
  if(clock<=0) {
    clearInterval(timer);
    hide_article();
  }
  if(clock<=178) { // 120초 경과후부터는 넘길 수 있음
    document.getElementById("finish-read").disabled = false;
  }
}, 1000);
}


