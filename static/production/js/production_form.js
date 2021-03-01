// let's take care of the order details first

function add_order(){
    var wrapper = document.getElementById('order-slug');
    var machine_id = document.getElementById('machine-id').innerHTML;
    // console.log("machine id",machine_id);
    var url = "http://127.0.0.1:8000/machines/1/production-form";

    fetch(url)
    .then((resp) => resp.json())
    .then(function(data){
        console.log('Data',data);
    });
}
