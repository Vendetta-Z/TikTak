function Like_product_btn(id){
    let Like_btn_by_id = document.getElementById('Like_product_btn_id_' + 'id')
    let Product_id = id
    let data = {
        Product_id: Product_id
        }

   $.ajax({
        method:'GET',
        dataType:'json',
        data: data,
        url: 'Like/add_like/',
        success:function(data){
            $('#Product_'+id+'_likes').text(data['two'])
            if (data['one'] == 'Product successful unliked'){
                $('#Like_product_btn_id_'+ id ).html('<i class="far fa-heart"></i>')
            }
            else{
                $('#Like_product_btn_id_'+ id).html('&#128147')
            }
        }
    })
   }



function Like_product_btn_remove(id){
    let Like_btn_by_id = document.getElementById('Like_product_btn_id_' + 'id')

   $.ajax({
        method:'GET',
        dataType:'json',
        data: {'Product_id':id, 'DLP':'1' },
        url: '/Like/add_like/',
        success:function(data){
        data['Like_product']

            $('#Product_'+id+'_likes').text(data['two'])
            if (data['one'] == 'Product successful unliked'){
                $('#block_with_liked_products').html('  ')
                let Like_product = JSON.parse(data['Like_product'])
                let Like_product_picture = JSON.parse(data['Like_product_pictures'])

                for(var i in Like_product){

                    $('#block_with_liked_products').append(''+
                        '<div class="col-md-3 recently_product">'+
                            '<div class="card mb-4 product-wap  rounded-0">'+
                                '<div class="card rounded-1">'+
                                    '<img class="card-img Product-image_sizing rounded-0 img-fluid" src="'+ Like_product_picture[Like_product[i]["pk"]] +'">'+
                                '<div class="card-img-overlay rounded-0 product-overlay d-flex align-items-center justify-content-center">'+
                                    '<ul class="list-unstyled">'+
                                         '<li><p class="btn btn-success text-white"'+
                                               'onclick="Like_product_btn_remove('+  Like_product[i]["pk"]  +')"'+
                                               'id="Like_product_btn_id_' + Like_product[i]["pk"] +'"'+
                                               'onload="is_like()"'+
                                               'Product_id=' +Like_product[i]["fields"]["id"] +'>&#128147</p></li>'+

                                        '<li><a class="btn btn-success text-white mt-2" href="'+  Like_product[i]["pk"]  +'/"><i class="far fa-eye"></i></a></li>'+
                                        '<li><a class="btn btn-success text-white mt-2" href="'+  Like_product[i]["pk"]  +'/"><i class="fas fa-cart-plus"></i></a></li>'+
                                    '</ul>'+
                                '</div>'+
                                '<div class="card-body">'+
                                    '<a href="' +Like_product[i]["pk"]+ '/" class="h3 text-decoration-none">'   +Like_product[i]["fields"]["Product_name"]+  '</a><br>'+
                                    '<ul class="w-100 list-unstyled d-flex justify-content-between mb-0">'+
                                        '<li>M/L/X/XL</li>'+
                                    '</ul>'+
                                    '<p class="text-center mb-0 price">'  +Like_product[i]["fields"]["Product_price"]+  'p.</p>'+
                                '</div>'+
                                '</div>'+
                            '</div>'+
                        '</div>')

            }
            }
            else{
                $('#Like_product_btn_id_'+ id).html('&#128147')
            }
        }
    })
   }