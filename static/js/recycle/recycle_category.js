document.addEventListener("DOMContentLoaded", function() {
    let recycleNavTrash = document.getElementById("recycle-nav-trash");
    let recycleSubNav = document.getElementById("recycle-sub-nav");
    let time;

    recycleNavTrash.addEventListener("mouseenter", function() {
        clearTimeout(time);
        recycleSubNav.style.display = "flex";
    });

    recycleNavTrash.addEventListener("mouseleave", function() {
        time = setTimeout(function() {
            recycleSubNav.style.display = "none";
        }, 200); 
    });

    recycleSubNav.addEventListener("mouseenter", function() {
        clearTimeout(time);
        recycleSubNav.style.display = "flex";
    });

    recycleSubNav.addEventListener("mouseleave", function() {
        time = setTimeout(function() {
            recycleSubNav.style.display = "none";
        }, 200);
    });
});

// #recycle-sub-nav에서 선택한 카테고리에 해당되는 .recycle-main을 나타나도록

document.addEventListener("DOMContentLoaded",function() {
    let nav1=document.getElementById("nav1");
    let recycleMain1=document.getElementById("recycle-main1");

    recycleMain1.style.display = "flex";

    nav1.addEventListener("click", function() {
        recycleMain1.style.display = "flex";
        recycleMain2.style.display = "none";
        recycleMain3.style.display = "none";
        recycleMain4.style.display = "none";
        recycleMain5.style.display = "none";
        recycleMain6.style.display = "none";
    });

    let nav2=document.getElementById("nav2");
    let recycleMain2=document.getElementById("recycle-main2");
    nav2.addEventListener("click", function() {
        recycleMain1.style.display = "none";
        recycleMain2.style.display = "flex";
        recycleMain3.style.display = "none";
        recycleMain4.style.display = "none";
        recycleMain5.style.display = "none";
        recycleMain6.style.display = "none";
    });

    let nav3=document.getElementById("nav3");
    let recycleMain3=document.getElementById("recycle-main3");
    nav3.addEventListener("click", function() {
        recycleMain1.style.display = "none";
        recycleMain2.style.display = "none";
        recycleMain3.style.display = "flex";
        recycleMain4.style.display = "none";
        recycleMain5.style.display = "none";
        recycleMain6.style.display = "none";
    });

    let nav4=document.getElementById("nav4");
    let recycleMain4=document.getElementById("recycle-main4");
    nav4.addEventListener("click", function() {
        recycleMain1.style.display = "none";
        recycleMain2.style.display = "none";
        recycleMain3.style.display = "none";
        recycleMain4.style.display = "flex";
        recycleMain5.style.display = "none";
        recycleMain6.style.display = "none";
    });

    let nav5=document.getElementById("nav5");
    let recycleMain5=document.getElementById("recycle-main5");
    nav5.addEventListener("click", function() {
        recycleMain1.style.display = "none";
        recycleMain2.style.display = "none";
        recycleMain3.style.display = "none";
        recycleMain4.style.display = "none";
        recycleMain5.style.display = "flex";
        recycleMain6.style.display = "none";
    });

    let nav6=document.getElementById("nav6");
    let recycleMain6=document.getElementById("recycle-main6");
    nav6.addEventListener("click", function() {
        recycleMain1.style.display = "none";
        recycleMain2.style.display = "none";
        recycleMain3.style.display = "none";
        recycleMain4.style.display = "none";
        recycleMain5.style.display = "none";
        recycleMain6.style.display = "flex";
    });


})