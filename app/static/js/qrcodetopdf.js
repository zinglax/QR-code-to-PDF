


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
  var data = {};

  function success(response){
    console.log("UPDATING: action_init");
    console.log(response['init']);
    $("#spa").empty();
    $("#spa").html(response['init']);
  }
  run_ajax_action("init", data, success);
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

  sleep(1000).then(() => {
    action_init()
  });


// End
});