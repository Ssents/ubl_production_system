
const date = new Date();
console.log(date);
// document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function(){
    $('#message').fadeOut('slow');
    }, 3000);

$('.datepicker').datetimepicker({
    dateFormat: "dd-mm-yy", 
    timeFormat: "HH:mm:ss"
});