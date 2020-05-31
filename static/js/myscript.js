// $(document).ready(function () {
//     $('.slick-slide').slick({
//         dots: true,
//         infinite: true,
//         speed: 300,
//         slidesToShow: 4,
//         slidesToScroll: 4,
//         responsive: [
//             {
//                 breakpoint: 1024,
//                 settings: {
//                     slidesToShow: 3,
//                     slidesToScroll: 3,
//                     infinite: true,
//                     dots: true
//                 }
//             },
//             {
//                 breakpoint: 600,
//                 settings: {
//                     slidesToShow: 2,
//                     slidesToScroll: 2
//                 }
//             },
//             {
//                 breakpoint: 480,
//                 settings: {
//                     slidesToShow: 1,
//                     slidesToScroll: 1
//                 }
//             }
//             // You can unslick at a given breakpoint now by adding:
//             // settings: "unslick"
//             // instead of a settings object
//         ]
//     });
// });

$(document).ready(function () {
    $('.product_carousel').owlCarousel({
        stagePadding: 10,
        loop: false,
        margin: 10,
        nav: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 3
            },
            1000: {
                items: 5
            }
        }
    });
});

// $(document).ready(function () {
//     const this_ = $("#article-good");
//     console.log(this_)
//     const goodUrl = this_.attr("data-href");
//     console.log(goodUrl)
//     $.ajax({
//         url: goodUrl,
//         method: "GET",
//         data: { "status": 0 },
//         success: function (data) {
//             if (data.liked) {
//                 const id = data.pk;
//                 const iconId = "#" + String(id);
//                 $(iconId).removeClass().addClass("fas fa-heart");
//             }
//         }, error: function (error) {
//             console.log("error")
//         }
//     })
// });

// $("#article-good").click(function (e) {
//     e.preventDefault()
//     const this_ = $(this);
//     const good_count = $("#good_count");
//     const goodUrl = this_.attr("data-href");
//     // const number = $("#article-good").children(i)
//     if (goodUrl) {
//         $.ajax({
//             url: goodUrl,
//             method: "GET",
//             data: { "status": 1 },
//             success: function (data) {
//                 const id = data.pk;
//                 const iconId = "#icon-" + String(id);
//                 const countId = "#good-count-" + String(id);
//                 const good_count = $(countId);
//                 let change_good = good_count.text();
//                 if (data.liked) {
//                     good_count.text(++change_good);
//                     $(iconId).removeClass().addClass("fas fa-heart");
//                 } else {
//                     good_count.text(--change_good);
//                     $(iconId).removeClass().addClass("far fa-heart");
//                 }
//             }, error: function (error) {
//                 console.log("error")
//             }
//         })
//     }
// })