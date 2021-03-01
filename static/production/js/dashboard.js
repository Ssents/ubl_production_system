// window.addEventListener('resize', function(event){
//     var element = document.getElementsByClassName("main-table-row");
//     element.classList.add("my-class");
//   });
// console.log($("#deleteConfirm").attr("href"))

$(".table tbody").on("click", "#deleteOrderButton",function(){
  var delete_link = $(this).closest('tr').find(".delete-url").attr("href");
  var id = $(this).closest('tr').attr("id");
  console.log(id, delete_link);
  $("#deleteConfirm").attr("href", delete_link);
});


var production_target = document.getElementById("productionTarget").innerHTML;
console.log(production_target);

var produced_tonage = document.getElementById("producedTonage").innerHTML;
console.log(produced_tonage);

var production_percentage = produced_tonage/production_target * 100;
console.log(production_percentage);



var element = $(".producedTonageCard");
console.log(element);

if (production_percentage > 95){
  console.log("Excellent");
  // element.classList.add("excellent");
  element.addClass('excellent');
}
else if (production_percentage<95 && production_percentage > 90){
  console.log("Just a little bit left");
  element.addClass("fair");

}
else{
  console.log("Poor perforamance");
  element.addClass("poor");

}