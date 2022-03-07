


function asynchronous_receiving_pagination_of_the_main_page(NewsPageNumber){
    let data = {
        NewsPageNumber:NewsPageNumber,
    }
    $.ajax({
        method:'GET',
        dataType:'json',
        data:data,
        url:'news/get_news_by_number',
        success:function(data){
            console.log('f')        
            console.log(data)
        }
    })
} 


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


function AddNewProductImage(product_id){
    var InputImage = document.getElementById('NewImageInput')

    formdata = new FormData()
    formdata.append('NewImage',InputImage.files[0])
    formdata.append('productID', product_id)

    $.ajax({
        url:'/AddNewProductImage/',
        type:'POST',
        data:formdata,
        processData: false,
        contentType: false,
        success:function(data){
                    let ProductImage_list = JSON.parse(data['ProductImageList'])
                    $('#ProductMainImage_img').html('<img class="main-card-img img-fluid" src="/'+ ProductImage_list[0]['fields']['image'] +'" alt="Card image cap">')
                    console.log(ProductImage_list)
                    $('#ProductImagesBlock').html(' ');
                    for (var image in ProductImage_list){
                        $('#ProductImagesBlock').append(''+
                            '<div class="col-4 old_product_images_div">'+
                                '<a>' + ProductImage_list[image]['pk']+ '</a>'+
                                '<input type="file" style="display:none;" id="' + ProductImage_list[image]['pk'] + ProductImage_list[image]['fields']['product'] +
                                '" onchange="ChangeProductImage('+ "'"+ProductImage_list[image]['fields']['product'] +"' ,"+"'"+ ProductImage_list[image]['pk']+"'"+')" name="newimage" id="ImageChangeInput"/>'+
                                '<label for="'+ ProductImage_list[image]['pk'] + ProductImage_list[image]['fields']['product'] +'"><img class="img-fluid" style="margin-top: 10px;" src="/' +ProductImage_list[image]['fields']['image']+ '" alt="Product Image 2">'+
                                                    '<a style="cursor: pointer;" onclick="DeleteProductImage('+ProductImage_list[image]["fields"]["product"]+','+ProductImage_list[image]['pk']+')">Удалить</a>')
                    }
                    $('#ProductImagesBlock').append(
                        '<div class="plus_div align-self-center">'+
                        '<label for="NewImageInput" class="plus">'+
                                '<input type="file" style="display:none;" name="NewAddingImage" id="NewImageInput" onchange="AddNewProductImage(product_id='+ProductImage_list[0]["fields"]["product"] +')"/>'+
                        '</label>'+
                        '</div>'
                        )   
        }
    })
}
    

function ChangeProductParams(P_id){
    let Product_id = P_id;
    let OldImageId = document.getElementById('oldImageId');

    let changed_product_name = document.getElementById('changed_product_name').value;
    let changed_for_which_gender = document.getElementById('changed_for_which_gender').value;
    let Product_price = document.getElementById('Product_price').value;
    let Product_brand = document.getElementById('Product_brand').value;
    let Product_color = document.getElementById('Product_color').value;
    let Product_characteristics = document.getElementById('Product_characteristics').value;

    formdata = new FormData();
    formdata.append('OldImageId', OldImageId);
    formdata.append('Product_name', changed_product_name);
    formdata.append('Product_price', Product_price);
    formdata.append('Product_color', Product_color);
    formdata.append('Product_brand', Product_brand);
    formdata.append('Product_characteristics', Product_characteristics);
    formdata.append('changed_for_which_gender', 'Boys');
    formdata.append('Product_id', Product_id);


    // for(let[key, value] of formdata){
    //     console.log(`${key}:${value}`)
    // }

    // for(let[key, value] of formdata){
    //     if (formdata.get(key) === ''){
    //         formdata.delete(key);
    //     }
    //     if(formdata.get(key) === null){
    //         formdata.delete(key)
    //     }
    // }
    // console.log('====================================')

    // for(let[key, value] of formdata){
    //     console.log(`${key}:${value}`)
    // }

    $.ajax({
        url: '/EditingProduct_ajax/',
        type: 'POST',
        data: formdata,
        
        processData: false,
        contentType: false,
        success:function(data){
            call_popup_with_text()
            var Product = data['product']
            $('#block_with_fields_for_changing_product_parameters').html(`<h1><input name='changed_product_name' id='changed_product_name' type="text" placeholder="`+ Product['fields']['Product_name']+ `"></h1>                                    
                                    <select name="changed_for_which_gender" id="changed_for_which_gender">
                                            <option value="Boys" >Для мальчиков</option>
                                            <option value="Girls" >Для девочек</option>
                                    </select>

                                    <!--{% if product.for_which_gender == 'Girls'%}
                                        <h6>Для девочек</h6>
                                    {% else %}
                                        <h6>Для Мальчиков</h6>
                                    {% endif %} -->

                                    <p class="h3 py-2">Цена: <input type="number" name="Product_price" id="Product_price" placeholder="`+ Product['fields']['Product_price'] +`"> p.</p>

                                    <ul class="list-inline">
                                        <li class="list-inline-item">
                                            <h6>Производитель:</h6>
                                        </li>
                                        <li class="list-inline-item">
                                            <p class="text-muted"><strong><input type="text" name="Product_brand" id="Product_brand" placeholder="`+ Product['fields']['Product_brand'] +`"></strong></p>
                                        </li>
                                    </ul>

                                    <h6>Описание:</h6>
                                    <p>`+ Product['fields']['Product_description'] +`</p>
                                    <ul class="list-inline">
                                        <li class="list-inline-item">
                                            <h6>Цвета :</h6>
                                        </li>
                                        <li class="list-inline-item">
                                            <p class="text-muted"><strong><input type="text" id="Product_color"  name="Product_color" placeholder="`+ Product['fields']['Product_color'] +`"></strong></p>
                                        </li>
                                    </ul>

                                    <h6>Характеристики:</h6><input type="text" name="Product_characteristics" id="Product_characteristics" placeholder="`+ Product['fields']['Product_characteristics'] +`">

                                        <input type="hidden" name="product-title" value="Activewear">
                                        <div class="row">
                                           
                                            </div>
                                        </div>
                                        <div class="row pb-3">
                                            <div class="col d-grid">
                                                <button  id="SubmitProductChangesBtn" onclick="ChangeProductParams('`+ Product['pk'] +`')" class="btn btn-success text-white mt-2" type="button"  name="">Подтвердить изменения</button>

                                                <!--<button type="submit" class="btn btn-success btn-lg" name="submit" value="addtocard">Add To Cart</button>-->
                                            </div>
                                        </div>`)

        }})
}
    



function ChangeProductImage(Product, Imageid){
    var inputbyid = document.getElementById(Imageid+Product);
    var formdata = new FormData();


    console.log(Imageid + Product)
    console.log(inputbyid)
    console.log('fuck')
    formdata.append('NewImage',inputbyid.files[0]);
    formdata.append('Imageid',Imageid);
    formdata.append('ProductId',Product);
    $.ajax({
        url: "/ChangeProductImage/",
        type: 'POST',
        data: formdata,
        processData: false,
        contentType: false,

        success:function(data){
                    let ProductImage_list = JSON.parse(data['ProductImages'])
                    $('#ProductMainImage_img').html('<img class="main-card-img img-fluid" src="/'+ ProductImage_list[0]['fields']['image'] +'" alt="Card image cap">')
                    console.log(ProductImage_list)
                    $('#ProductImagesBlock').html(' ');
                    for (var image in ProductImage_list){
                        $('#ProductImagesBlock').append(''+
                            '<div class="col-4 old_product_images_div">'+
                                '<a>' + ProductImage_list[image]['pk']+ '</a>'+
                                '<input type="file" style="display:none;" id="' + ProductImage_list[image]['pk'] + ProductImage_list[image]['fields']['product'] +
                                '" onchange="ChangeProductImage('+ "'"+ProductImage_list[image]['fields']['product'] +"' ,"+"'"+ ProductImage_list[image]['pk']+"'"+')" name="newimage" id="ImageChangeInput"/>'+
                                '<label for="'+ ProductImage_list[image]['pk'] + ProductImage_list[image]['fields']['product'] +'"><img class="img-fluid" style="margin-top: 10px;" src="/' +ProductImage_list[image]['fields']['image']+ '" alt="Product Image 2">'+
                                                    '<a style="cursor: pointer;" onclick="DeleteProductImage('+ProductImage_list[image]["fields"]["product"]+','+ProductImage_list[image]['pk']+')">Удалить</a>')
                    }
                    $('#ProductImagesBlock').append(
                        '<div class="plus_div align-self-center">'+
                        '<label for="NewImageInput" class="plus">'+
                                '<input type="file" style="display:none;" name="NewAddingImage" id="NewImageInput" onchange="AddNewProductImage(product_id='+ProductImage_list[0]["fields"]["product"] +')"/>'+
                        '</label>'+
                        '</div>'
                        )
                } 
    })
    call_popup_with_text()
        
    }

function DeleteProductImage(Product,Imageid){
    $.ajax({
        url: "/DeleteProductImage/",
        type: 'POST',
        data: {'ImageId':Imageid,'ProductId':Product},
        success:function(data){
                    let ProductImage_list = JSON.parse(data['ProductImageList'])
                    $('#ProductMainImage_img').html('<img class="main-card-img img-fluid" src="/'+ ProductImage_list[0]['fields']['image'] +'" alt="Card image cap">')
                    console.log(ProductImage_list)
                    $('#ProductImagesBlock').html(' ');
                    for (var image in ProductImage_list){
                        $('#ProductImagesBlock').append(''+
                            '<div class="col-4 old_product_images_div">'+
                                '<a>' + ProductImage_list[image]['pk']+ '</a>'+
                                '<input type="file" style="display:none;" id="' + ProductImage_list[image]['pk'] + ProductImage_list[image]['fields']['product'] +
                                '" onchange="ChangeProductImage('+ "'"+ProductImage_list[image]['fields']['product'] +"' ,"+"'"+ ProductImage_list[image]['pk']+"'"+')" name="newimage" id="ImageChangeInput"/>'+
                                '<label for="'+ ProductImage_list[image]['pk'] + ProductImage_list[image]['fields']['product'] +'"><img class="img-fluid" style="margin-top: 10px;" src="/' +ProductImage_list[image]['fields']['image']+ '" alt="Product Image 2">'+
                                                    '<a style="cursor: pointer;" onclick="DeleteProductImage('+ProductImage_list[image]["fields"]["product"]+','+ProductImage_list[image]['pk']+')">Удалить</a>')
                    }
                    $('#ProductImagesBlock').append(
                        '<div class="plus_div align-self-center">'+
                        '<label for="NewImageInput" class="plus">'+
                                '<input type="file" style="display:none;" name="NewAddingImage" id="NewImageInput" onchange="AddNewProductImage(product_id='+ProductImage_list[0]["fields"]["product"] +')"/>'+
                        '</label>'+
                        '</div>'
                        )
        }
    })}

function call_popup_with_text(SomeText){
    let popup = document.getElementById('Popup_function_notification')
    popup.innerHTML ='Изменения были успешно добавлены'
    popup.style.display = "block"
    AnimatePopup(popup, 5 , 3000)
    setTimeout(()=>{popup.style.display = "none"}, 2000);}

function AnimatePopup(variable , animationspeed, second ){
    let start = Date.now();
    let timer = setInterval(function() {
  // сколько времени прошло с начала анимации?
      let timePassed = Date.now() - start;

    if (timePassed >= second) {
        clearInterval(timer); // закончить анимацию через 2 секунды
        return;
    }
    // отрисовать анимацию на момент timePassed, прошедший с начала анимации
  draw(timePassed);

    }, 20);

    // в то время как timePassed идёт от 0 до 2000
    // left изменяет значение от 0px до 400px
    function draw(second) {
      variable.style.right = second / animationspeed + 'px';
    }
    draw(second)}