  function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
  }

  // SHOULD 180
  var CLOCK = 180;
  var clock=CLOCK;
  var breaktime = 300; //5분
  var tnv=[];
  var tnv_urls=[];
  // SHOULD 17
  var tnv_size = 17;
  var trap1 = "", trap2 = "";
  var nonsense1=4, nonsense2=6, nonsense3=2, nonsense4=2, nonsense5=5, nonsense6=1;
  var nonsense_clicked = true;
  var task_num = 1;

  for(var i=0; i<tnv_size; ++i){
    tnv[i] = i+1;
  }
  shuffleArray(tnv);
  console.log(tnv);

  var tnv_idx = 0;
  var val1=0, val2=0, val3=0, val4=0, val5=0;
  var article=Math.floor(Math.random() * 2) + 1;

  function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }

  function show_article(){
    document.getElementById("finish-read").disabled = true;
    $('#show-article').css("display", "none");
    $('#article-'+article).css("display", "block");
    $('#finish-read-div').css("display", "block");
    $('#article-instruction').css("display", "none");
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

  function count_breaktime(){
    var timer = setInterval(function() {
      breaktime--;
      $('#breaktimeLeft').html("Time Left : " + breaktime);
      if(breaktime<0) {
        clearInterval(timer);
        NextTask();
      }
    }, 1000);
  }

  function allChecked(){
    if(val1>0 && val2>0 && val3>0 && val4>0 && val5>0 && nonsense_clicked)
      return true;
    else
      return false;
  }

  function changeTnv() {
    console.log(tnv_idx);
    console.log(tnv[tnv_idx]);

    $('#task-img').attr("src","/static/images/tnv"+article+"/"+tnv[tnv_idx]+".png")

    $('#tn-title').text("Thumbnail " + (tnv_idx+1) + " / 18");

    //$('.tn').css("border", "none");
    //$('#tn-'+article+'-'+tnv[tnv_idx]).css("border","2px solid red");

    $('#button-1 button').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      val1 = $(this).text();
    });

    $('#button-2 button').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      val2 = $(this).text();
    });

    $('#button-3 button').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      val3 = $(this).text();
    });

    $('#button-4 button').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      val4 = $(this).text();
    });

    $('#button-5 button').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      val5 = $(this).text();
    });
  }

  function attentionCheck() {
    var ran =Math.floor(Math.random() *  tnv_size) + 1;
    $('#check'+article+'id').val(ran);

    $('#task-img').attr("src","/static/images/tnv"+article+"/"+ran+".png")

    $('#tn-title').text("Thumbnail 18 / 18");

    //$('.tn').css("border", "none");
    //$('#tn-'+article+'-'+ran).css("border","2px solid red");

    $('#button-1 button').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      val1 = $(this).text();
    });

    $('#button-2 button').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      val2 = $(this).text();
    });

    $('#button-3 button').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      val3 = $(this).text();
    });

    $('#button-4 button').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      val4 = $(this).text();
    });

    $('#button-5 button').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      val5 = $(this).text();
    });

  }

   function checkValid(){
       $('.instruction').css("display", "block");

   // 버튼 활성화 및 valid 질문 보여주기
       if(article==1){
            $("#valid-row1").css("display", "block");
            $('#trapbtn1 button').click(function() {
              $(this).addClass('active').siblings().removeClass('active');
              trap1 = $(this).text();
            });
       }else{
            $("#valid-row2").css("display", "block");
            $('#trapbtn2 button').click(function() {
              $(this).addClass('active').siblings().removeClass('active');
              trap2 = $(this).text();
            });
       }
   }

  function hide_article(){
    $('#task-article').css("display", "none");
    $('#article-'+article).css("display", "none");
    $('#timeLeft').html("Time is done");
    $('#finish-read-div').css("display", "none");
    checkValid();
  }

  function NextTask(){
      $('#task-article').css("display", "block");
      $('#show-article').css("display", "block");
      $('#break-time').css("display", "none");
      tnv_idx = 0;
      shuffleArray(tnv);
      task_num++;
      if(article==1)
        article = 2;
      else
        article = 1;
  }

  function FinishTask(){
      $('#final-div').css("display", "block");

        // SHOULD removed!
        /*
        for(var i=0; i<17; ++i){
             $('#a1g1t'+(i+1)).val(Math.floor(Math.random() * 7) + 1);
             $('#a1g2t'+(i+1)).val(Math.floor(Math.random() * 7) + 1);
             $('#a1g3t'+(i+1)).val(Math.floor(Math.random() * 7) + 1);
             $('#a1g4t'+(i+1)).val(Math.floor(Math.random() * 7) + 1);
             $('#a1g5t'+(i+1)).val(Math.floor(Math.random() * 7) + 1);

             $('#a2g1t'+(i+1)).val(Math.floor(Math.random() * 7) + 1);
             $('#a2g2t'+(i+1)).val(Math.floor(Math.random() * 7) + 1);
             $('#a2g3t'+(i+1)).val(Math.floor(Math.random() * 7) + 1);
             $('#a2g4t'+(i+1)).val(Math.floor(Math.random() * 7) + 1);
             $('#a2g5t'+(i+1)).val(Math.floor(Math.random() * 7) + 1);
          }
          */

  }

  function saveAns(){
    if(tnv_idx==tnv_size){ //validation check
     if(article==1){
          $('#check1val1').val(val1);
          $('#check1val2').val(val2);
          $('#check1val3').val(val3);
          $('#check1val4').val(val4);
          $('#check1val5').val(val5);

        }else{
          $('#check2val1').val(val1);
          $('#check2val2').val(val2);
          $('#check2val3').val(val3);
          $('#check2val4').val(val4);
          $('#check2val5').val(val5);

        }
    }else{
     if(article==1){
      $('#a1g1t'+tnv[tnv_idx]).val(val1);
      $('#a1g2t'+tnv[tnv_idx]).val(val2);
      $('#a1g3t'+tnv[tnv_idx]).val(val3);
      $('#a1g4t'+tnv[tnv_idx]).val(val4);
      $('#a1g5t'+tnv[tnv_idx]).val(val5);

    }else{
      $('#a2g1t'+tnv[tnv_idx]).val(val1);
      $('#a2g2t'+tnv[tnv_idx]).val(val2);
      $('#a2g3t'+tnv[tnv_idx]).val(val3);
      $('#a2g4t'+tnv[tnv_idx]).val(val4);
      $('#a2g5t'+tnv[tnv_idx]).val(val5);

    }
  }
    val1 = 0;
    val2 = 0;
    val3 = 0;
    val4 = 0;
    val5 = 0;
  }

  $("#start" ).click(function() {
    $("#information").css("display", "none");
    $('#task-article').css("display", "block");
  });

  $("#show-article" ).click(function() {
    show_article();
  });

  $('#trap-ans1').click(function(){
    if(trap1!=""){

        // wrong answer -> fail!
        if(trap1!="Immigration"){
            $('#passTrap').val(false);
            $( "#ans-form" ).submit();
            $('#valid1').val(trap1);
        }else{
            $("#valid-row1").css("display", "none");
            $('#valid1').val(trap1);
            $('#task-article').css("display", "block");
            $('#task-instruction').css("display", "block");
            $("#gotoTask").css("display", "block");
            $('#timeLeft').html("");
        }
    }
  });


  $('#trap-ans2').click(function(){
    if(trap2!=""){

        // wrong answer -> fail!
        if(trap2!="Internet rate"){
            $('#passTrap').val(false);
            $( "#ans-form" ).submit();
            $('#valid2').val(trap2);
        }
        else{
            $("#valid-row2").css("display", "none");
            $('#valid2').val(trap2);
            $("#gotoTask").css("display", "block");
            $('#task-article').css("display", "block");
            $('#task-instruction').css("display", "block");
            $('#timeLeft').html("");
        }
    }
  });

  $("#gotoTask" ).click(function() {
    $('#timeLeft').html("");
    $('#article-instruction').css("display", "block");
    $('#task-instruction').css("display", "none");
    $('#task-article').css("display", "none");
    $('#task-tnvs').css("display", "block");
    $('#ranking-button').css("display", "block");
    //$('.tnv-container'+article).css("display", "block");
    $('#gotoTask').css("display", "none");

    changeTnv();
  });

  $("#gotoNext" ).click(function() {
    $('.nonsense').css("display", "none");
    $('#nonsense-1').css("display", "none");
    $('#nonsense-2').css("display", "none");
    $('#nonsense-3').css("display", "none");
    $('#nonsense-4').css("display", "none");
    $('#nonsense-5').css("display", "none");
    $('#nonsense-6').css("display", "none");

    if(allChecked()){
      $('button').removeClass('active');
      saveAns();
      // Nonsense 문제가 틀리지 않은 경우, 정상진행
      if(nonsense1==4 && nonsense2==6 && nonsense3==2 && nonsense4==2 && nonsense5==5 && nonsense6==1){
          //attention check
          if(tnv_idx==tnv_size-1){ // 17번쨰 썸네일인지
           if(task_num==1) {
             $('.nonsense').css("display", "block");
             $('#nonsense-3').css("display", "block");
           }else {
            $('.nonsense').css("display", "block");
            $('#nonsense-6').css("display", "block");
           }
            attentionCheck(); // 중복 썸네일
            tnv_idx++; //중복 썸네일 18번쨰
            topFunction();
          }else if(tnv_idx>tnv_size-1) { // 18번째까지 봤는지
            $('#task-tnvs').css("display", "none");
            $('#ranking-button').css("display", "none");

            if(task_num==1){ // ARTICLE 몇개 봤는지
                $('#break-time').css('display', 'block');
                count_breaktime();
            }else{ //
                FinishTask();
            }

          }else {

            if(tnv_idx==5){
                if(task_num==1) {
                 $('.nonsense').css("display", "block");
                 $('#nonsense-1').css("display", "block");
                 nonsense_clicked = false;
                }else {
                 $('.nonsense').css("display", "block");
                 $('#nonsense-4').css("display", "block");
                 nonsense_clicked = false;
                }
            }

             else if(tnv_idx==11){
                if(task_num==1) {
                 $('.nonsense').css("display", "block");
                 $('#nonsense-2').css("display", "block");
                 nonsense_clicked = false;
                }else {
                 $('.nonsense').css("display", "block");
                 $('#nonsense-5').css("display", "block");
                 nonsense_clicked = false;
                }
            }
            tnv_idx++;
            changeTnv();
            topFunction();
          }
      }else{ // nonsense 문제가 틀렸을 경우 함정을 못 피한 것으로 간주, 강제종료
            $('#passTrap').val(false);
            $( "#ans-form" ).submit();
      }
    }else{
      alert('Please submit ratings for each statement');
    }
  });

  $('#finish-break').click(function() {
    breaktime = 0;
  })

  $("#finish-read").click(function() {
    clock = 0;
    hide_article();
  })

$('#button-nonsense-1 button').click(function () {
    $(this).addClass('active').siblings().removeClass('active');
    nonsense1 = $(this).text();
    nonsense_clicked = true;
    $('#nonsenseNum').val(1);
})

$('#button-nonsense-2 button').click(function () {
    $(this).addClass('active').siblings().removeClass('active');
    nonsense2 = $(this).text();
    nonsense_clicked = true;
    $('#nonsenseNum').val(2);
})

$('#button-nonsense-3 button').click(function () {
    $(this).addClass('active').siblings().removeClass('active');
    nonsense3 = $(this).text();
    nonsense_clicked = true;
    $('#nonsenseNum').val(3);
})

$('#button-nonsense-4 button').click(function () {
    $(this).addClass('active').siblings().removeClass('active');
    nonsense4 = $(this).text();
    nonsense_clicked = true;
    $('#nonsenseNum').val(4);
})

$('#button-nonsense-5 button').click(function () {
    $(this).addClass('active').siblings().removeClass('active');
    nonsense5 = $(this).text();
    nonsense_clicked = true;
    $('#nonsenseNum').val(5);
})

$('#button-nonsense-6 button').click(function () {
    $(this).addClass('active').siblings().removeClass('active');
    nonsense6 = $(this).text();
    nonsense_clicked = true;
    $('#nonsenseNum').val(6);
})


