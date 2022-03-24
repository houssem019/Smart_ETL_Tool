
$("form[name=signup_form").submit(function(e) {
  alert("Registred Successfully");

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/extract";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=login_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signin",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/extract";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

var a=1;
function show_hide(){
  if(a==1){
    document.getElementById("cont2").style.display="inline";
    document.getElementById("cont1").style.display="none";
    return a=0;
  }
  else{
    document.getElementById("cont2").style.display="none";
    document.getElementById("cont1").style.display="inline";
    return a=1;
  }

}

function activate(){
  document.getElementById("download").className+="btn btn-primary btn-block";
  alert("Registred Successfully");

}
window.onload = function() {
  document.getElementById('download').addEventListener('click',activate);
}
