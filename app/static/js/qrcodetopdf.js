


/**
 * Run an AJAX Action
 * @param  {[type]} action       [description]
 * @param  {[type]} data         [description]
 * @param  {[type]} success_func [description]
 * @return {[type]}              [description]
 */
function run_ajax_action(action, data, success_func){
  var d = {"action": action,
           "data": data};
  $.ajax({
      url: window.location.pathname,
      contentType: 'application/json',
      dataType : 'json',      
      data: JSON.stringify(d),  
      type: 'POST',
      success: function(response) {
          // Save the local_data to localStorage
          console.log("ajax action: " + d["action"] + " success")
          if (success_func){
            success_func(response);
          }
      },
      error: function(error) {
          console.log("ajax action: " + d["action"] + " failure")
          console.log(error);
      }
  }); 
}


function action_init(){
  var data = {}
  ;
  function success(response){
    console.log("UPDATING: action_init");
    console.log(response['init']);
    $("#spa").empty();
    $("#spa").html(response['init']);
  }
  run_ajax_action("init", data, success);
}


function action_render(){

  console.log($($("#qr-pdf-size")[0]).val());
  console.log($($("#qr-pdf-number")[0]).val());
  console.log($($("#qr-pdf-fg-color")[0]).val());
  console.log($($("#qr-pdf-bg-color")[0]).val());
  console.log($($("#qr-pdf-label-text")[0]).val());



  var data = {
    "size": $($("#qr-pdf-size")[0]).val(),
    "number": $($("#qr-pdf-number")[0]).val(),
    "fg_color": $($("#qr-pdf-fg-color")[0]).val(),
    "bg_color": $($("#qr-pdf-bg-color")[0]).val(),
    "text": $($("#qr-pdf-label-text")[0]).val()
  }
  ;
  function success(response){
    console.log( "UPDATING: action_render" );
    console.log( response['render'] );
    $( "#spa" ).empty();
    $( "#spa" ).html( response['render']);
  }
  run_ajax_action("render", data, success);
}


function init_spectrum(jqSelector){
  console.log("initializing");

  // $(jqSelector).spectrum({
  //   showInput: true,
  //   allowEmpty:true,
  //   showAlpha: true
  // });
  // 
  $("#qr-pdf-bg-color").spectrum({
    color: "#f00"
});
}


/** 
 * Sleep time expects milliseconds
 * @param  {[type]}
 * @return {[type]}
 */
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}


/** Workspace Main
 * occurs on jquery's document pagecreate
 * 
 */
$( document ).ready(function() {

  sleep(90).then(() => {
    action_init();
  });

  sleep(100).then(() => {
    $( "#qr-pdf-render" ).click(function (){
      action_render();
    });
  });

init_spectrum(".qr-pdf-spectrum")

// End
});