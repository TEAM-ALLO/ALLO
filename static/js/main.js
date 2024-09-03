document.addEventListener('DOMContentLoaded', function() {
    const hamburgerBtn = document.getElementById('hamburger-btn');
    const sidebar = document.getElementById('sidebar');
    
    hamburgerBtn.addEventListener('click', function() {
        sidebar.style.display = sidebar.style.display === 'inline-flex' ? 'none' : 'inline-flex';
        
        hamburgerBtn.classList.toggle('open');
    });
});


// 헤더의 돋보기 버튼 클릭하면 검색창 나타나도록
document.addEventListener('DOMContentLoaded', function() {
    let searchLogo=document.getElementById("search_logo");
    let searchLogo2=document.getElementById("search_logo2");
    let headerNavSearch=document.getElementById("header-nav-search");
    let headerNavSearchIcon=document.getElementById("header-nav-search-icon");

    searchLogo2.addEventListener("click", function() {
        searchLogo2.style.display = "none";
        searchLogo.style.display = "flex";
        headerNavSearch.style.display = "flex";
        headerNavSearchIcon.style.display = "flex";
    });

    // 검색 폼 밖의 클릭 시 검색 폼 숨기기 (선택 사항)
    document.addEventListener('click', function(event) {
        if (!headerNavSearchForm.contains(event.target) && !searchLogo2.contains(event.target)) {
            searchLogo2.style.display = 'flex'; // 돋보기 아이콘 보이기
            searchLogo.style.display = 'none';  // 검색창 숨기기
            headerNavSearchForm.style.display = 'none'; // 검색 폼 숨기기
        }
    });
});