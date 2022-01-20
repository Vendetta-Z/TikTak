





function output_added_picture_for_the_product(input){
    product_image_input_div = document.getElementById('selected_picture_for_product_div')
    product_image_input = document.getElementById('selected_picture_for_product')
    

    html_code_to_display_the_selected_picture = '<img class="img-fluid" name="product_image" id="entering_file_img" alt="Изображение товара" src="' + product_image_input.files[0].name + ' " class="product_image" /> '
    fuck = '<input type="file" style="display:none;" name="additional_images_for_the_product" accept="image/*" value="'+ product_image_input.value +'"/>'
    console.log(product_image_input.files[0].name)
    product_image_input_div.insertAdjacentHTML( "afterbegin", html_code_to_display_the_selected_picture)
    product_image_input_div.insertAdjacentHTML( "afterbegin", fuck)
    

    if (input.files && input.files[0]) {
            var reader = new FileReader();

           reader.onload = function (e) {
                $('#entering_file_img')
                    .attr('src', e.target.result)
                    .width(150)
                    .height(200);
            };


            reader.readAsDataURL(input.files[0]);
        }
}

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





function DeleteProduct(id){

   $.ajax({
        method:'GET',
        dataType:'json',
        data: {'Product_id':id},
        url: "/DeleteProduct/",
        success:function(data){
                $('#block_with_list_of_added_products').html('  ')
                let Product_list = JSON.parse(data['ProductList'])
                let Product_img = JSON.parse(data['ProductImages'])
                console.log(Product_list)
                console.log(Product_img)

                for(var i in Product_list){

                    $('#block_with_list_of_added_products').append(''+
                        '<div class="col-md-3 recently_product">'+
                            '<div class="card mb-4 product-wap  rounded-0">'+
                                '<div class="card rounded-1">'+
                                    '<img class="card-img Product-image_sizing rounded-0 img-fluid" src="'+ Product_img[Product_list[i]['pk']] +'">'+
                                '<div class="card-img-overlay rounded-0 product-overlay d-flex align-items-center justify-content-center">'+
                                    '<ul class="list-unstyled">'+
                                         '<li><p class="btn btn-success text-white"'+
                                               'onclick="Like_product_btn_remove('+ Product_list[i]['id']  +')"'+
                                               'id="Like_product_btn_id_' + Product_list[i]['id'] +'"'+
                                               'onload="is_like()"'+
                                               'Product_id=' + Product_list[i]['id'] +'>&#128147</p></li>'+

                                        '<li><a class="btn btn-success text-white mt-2" href="'+  Product_list[i]['id']  +'/"><i class="far fa-eye"></i></a></li>'+
                                        '<li><a class="btn btn-success text-white mt-2" href="'+  Product_list[i]['id']  +'/"><i class="fas fa-cart-plus"></i></a></li>'+
                                    '</ul>'+
                                '</div>'+
                                '<div class="card-body">'+
                                    '<a href="' +Product_list[i]['id']+ '/" class="h3 text-decoration-none">'   + Product_list[i]["fields"]["Product_name"]+  '</a><br>'+
                                    '<ul class="w-100 list-unstyled d-flex justify-content-between mb-0">'+
                                        '<li>M/L/X/XL</li>'+
                                    '</ul>'+
                                    '<p class="text-center mb-0 price">'  +Product_list[i]["fields"]["Product_price"]+  'p.</p>'+
                                '</div>'+
                                '</div>'+
                            '</div>'+
                        '</div>')

            }
        }
    })
   }


function AddOrChangeProductImage(product_id,Image,O_P_P){
        var ImageChangeInput = document.getElementById('ImageChangeInput')
        var NewImageInput = document.getElementById('NewImageInput')
        var formdata = new FormData();


        file = ImageChangeInput.files[0];
        NewImageFile = NewImageInput.files[0]

        console.log(Image)

        formdata.append('upload_image', file);
        formdata.append('Product_id', product_id);
        formdata.append('Old_product_picture', Image);
        formdata.append('NewAddingImage', NewImageFile)
        $.ajax({
            url: "/ChangeProductImage/",
            type: 'POST',
            data: formdata,
            processData: false,
            contentType: false,
            success: console.log('success!')
        });

}
    