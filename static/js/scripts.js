//ver contraseña 
document.addEventListener("DOMContentLoaded", function () {
    const pass1 = document.getElementById("pass1");
    const pass2 = document.getElementById("pass2");
    const checkbox = document.getElementById("showPasswordCheckbox");

    checkbox.addEventListener("change", function(){
        if(checkbox.checked){
            pass1.type = "text";
            pass2.type = "text";
        }else{
            pass1.type = "password";
            pass2.type = "password";
        }
    });
});







