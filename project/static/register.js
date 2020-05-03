function check() {
    if(document.getElementById('firstname').value=="" || document.getElementById('firstname').value==undefined 
        ||document.getElementById('lastname').value=="" || document.getElementById('lastname').value==undefined 
        ||document.getElementById('email').value=="" || document.getElementById('email').value==undefined 
    	|| document.getElementById('password').value=="" || document.getElementById('password').value==undefined 
    	|| document.getElementById('password2').value=="" || document.getElementById('password2').value==undefined) {
        alert("Please complete all fields.");
        return false;
    }
    else if(document.getElementById('password').value!=document.getElementById('password2').value) {
    	alert("Passwords do not match.")
    	return false;
    }
    return true;
}