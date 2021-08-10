function allChecked1() {
    if(q1 !="")
        return true;
    else
        return false;
}
function allChecked2() {
    if($("#text-q2").val().length>70)
        return true;
    else
        return false;
}
function allChecked3() {
    if ($("#text-1").val()==" " && $("#text-2").val().length > 70 && $("#text-3").val().length > 70 && $("#text-4").val().length>70) {
        $("#text-1").val("None")
        return true; }
    else if ($("#text-2").val()==" " && $("#text-1").val().length > 70 && $("#text-3").val().length > 70 && $("#text-4").val().length>70) {
        $("#text-2").val("None")
        return true; }
    else if ($("#text-3").val()==" " && $("#text-1").val().length > 70 && $("#text-2").val().length > 70 && $("#text-4").val().length>70) {
        $("#text-3").val("None")
        return true;}
    else if ($("#text-4").val()==" " && $("#text-1").val().length > 70 && $("#text-2").val().length > 70 && $("#text-3").val().length>70) {
        $("#text-4").val("None")
        return true; }
    else
        return false;
}

function tnSelected() {
    if(q1 == "A")
        $("#tn1").attr('style', "max-width:100%; height:100mm; width:83mm; border:2px solid; border-color:red");
    else if(q1 == "B")
        $("#tn2").attr('style', "max-width:100%; height:100mm; width:83mm; border:2px solid; border-color:red");
    else if(q1 == "C")
        $("#tn3").attr('style', "max-width:100%; height:100mm; width:83mm; border:2px solid; border-color:red");
    else if(q1 == "D")
        $("#tn4").attr('style', "max-width:100%; height:100mm; width:83mm; border:2px solid; border-color:red");
}

function showQuestions() {
    if (q1 != "A")
        $("#q3-A").css("display", "block");
    if (q1 != "B")
        $("#q3-B").css("display", "block");
    if (q1 != "C")
        $("#q3-C").css("display", "block");
    if (q1 != "D")
        $("#q3-D").css("display", "block");
}

var numlist = ["1","2","3","4"]
var alphlist = {"A":"1","B":"2","C":"3","D":"4"}

function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
  }
  shuffleArray(numlist);

  var mylist={"A":numlist[0],"B":numlist[1],"C":numlist[2],"D":numlist[3]}
   console.log(mylist)
var q1=""
var trap=""

$("#btn-show-compare").click(function(){
    $("#compare-instruction").css("display", "none");
    $("#show-compare").css("display", "block");

    $("#tn"+mylist['A']).attr("src","/static/editedTN/a.png")
    $("#tn"+mylist['B']).attr("src","/static/editedTN/b.png")
    $("#tn"+mylist['C']).attr("src","/static/editedTN/c.png")
    $("#tn"+mylist['D']).attr("src","/static/editedTN/d.png")
});

$("#btn-show-nonsense").click(function() {
    if(allChecked1()) {
        Object.keys(mylist).map(function(key, index) {
          if(mylist[key] == alphlist[q1])
            $("#q1").val(key);
        });
        $("#question-1").css("display", "none");
        $("#nonsense").css("display", "block");
    }
    else
        alert("Please answer the question.");
});

$("#btn-show-question-2").click(function(){
    if(trap != "None") {
        $("#trap").val(trap)
        if(trap != "A"){
            $("#passTrap").val(false);
            $("#ans-form").submit();
        } else {
            $("#nonsense").css("display", "none");
            $("#question-2").css("display", "block");
            $("#question2").html("Why would you choose \"" + q1 +"\"? (minimum 70 characters)")
            tnSelected();    }
    }
    else
        alert("Please answer the question.");
});

$("#btn-show-question-3").click(function(){
    if (allChecked2()) {
        $("#q2").val($("#text-q2").val())
        $("#question-2").css("display", "none");
        $("#question-3").css("display", "block");
        showQuestions();
    } else
        alert('Please write your answers more than 70 characters.');
});

$("#btn-finish-task").click(function() {
    if (allChecked3()) {
        $("#q3a").val($("#text-"+mylist["A"]).val());
        $("#q3b").val($("#text-"+mylist["B"]).val());
        $("#q3c").val($("#text-"+mylist["C"]).val());
        $("#q3d").val($("#text-"+mylist["D"]).val());
        $("#show-compare").css("display", "none");
        $("#final-div").css("display", "block");
    } else
         alert('Please write down all answers more than 70 characters');
});

$('#button-1 button').click(function() {
  $(this).addClass('active').siblings().removeClass('active');
  q1 = $(this).text();
});
$('#button-2 button').click(function() {
  $(this).addClass('active').siblings().removeClass('active');
  trap = $(this).text();
});


$("#text-q2").keyup(function(e) {
    var content = $(this).val();
   $('#counter-q2').html("("+content.length+" / 300 characters)");
   $(this).val(content.substring(0, 300));
});
$("#text-1").keyup(function(e) {
    var content = $(this).val();
   $('#counter-a').html("("+content.length+" / 300 characters)");
   $(this).val(content.substring(0, 300));
});
$("#text-2").keyup(function(e) {
    var content = $(this).val();
   $('#counter-b').html("("+content.length+" / 300 characters)");
   $(this).val(content.substring(0, 300));
});
$("#text-3").keyup(function(e) {
    var content = $(this).val();
   $('#counter-c').html("("+content.length+" / 300 characters)");
   $(this).val(content.substring(0, 300));
});
$("#text-4").keyup(function(e) {
    var content = $(this).val();
   $('#counter-d').html("("+content.length+" / 300 characters)");
   $(this).val(content.substring(0, 300));
});