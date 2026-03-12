// CAPTCHA VARIABLES
let captchaText = "";
let generatedOTP = "";

// GENERATE CAPTCHA
function generateCaptcha(){

let chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

captchaText = "";

for(let i=0;i<5;i++){
captchaText += chars.charAt(Math.floor(Math.random()*chars.length));
}

document.getElementById("captcha").innerText = captchaText;

}

// CALL CAPTCHA FUNCTION
generateCaptcha();


// SEND OTP FUNCTION
function sendOTP(){

generatedOTP = Math.floor(100000 + Math.random()*900000);

alert("Your OTP is: " + generatedOTP);

}


// FORM VALIDATION
document.getElementById("registerForm").addEventListener("submit",function(e){

e.preventDefault();

let password = document.getElementById("password").value;
let confirmPassword = document.getElementById("confirmPassword").value;
let userCaptcha = document.getElementById("captchaInput").value;
let userOTP = document.getElementById("otp").value;

if(password !== confirmPassword){
alert("Passwords do not match");
return;
}

if(userCaptcha !== captchaText){
alert("Captcha incorrect");
generateCaptcha();
return;
}

if(userOTP != generatedOTP){
alert("Invalid OTP");
return;
}

alert("Registration Successful!");

});