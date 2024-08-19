// 선택한 카테고리의 게시글만 보이도록 구현
// 선택한 카테고리의 글자색은 검정색, 선택하지 않은 카테고리의 글자색은 회색
document.addEventListener("DOMContentLoaded",function() {
    let myPosts=document.getElementById("my_posts");
    let bookmarked=document.getElementById("bookmarked");

    let subCategoryPost=document.getElementById("sub-category-post");
    let subCategoryookmark=document.getElementById("sub-category-bookmark");
    
    let myPost1=document.getElementById("mypost1");
    let myPost2=document.getElementById("mypost2");
    let myPost3=document.getElementById("mypost3");
    let myPost4=document.getElementById("mypost4");

    let mybookmarked1=document.getElementById("mybookmarked1");
    let mybookmarked2=document.getElementById("mybookmarked2");
    let mybookmarked3=document.getElementById("mybookmarked3");
    let mybookmarked4=document.getElementById("mybookmarked4");

    let postsAll=document.getElementById("posts-all");
    let postsCommunity=document.getElementById("posts-community");
    let postsRecipe=document.getElementById("posts-recipe");
    let postsInterior=document.getElementById("posts-interior");
    
    let bookmarksAll=document.getElementById("bookmarks-all");
    let bookmarksCommunity=document.getElementById("bookmarks-community");
    let bookmarksRecipe=document.getElementById("bookmarks-recipe");
    let bookmarksInterior=document.getElementById("bookmarks-interior");

    let mypageAllPost=document.getElementById("mypage-all-post");

    let gridIcon=document.getElementById("grid-icon");
    let bookmarkIcon=document.getElementById("bookmark-icon");

    // 내 글
    myPosts.addEventListener("click", function() {
        subCategoryPost.style.display = "flex";
        subCategoryookmark.style.display = "none";
        myPost1.style.display = "flex";
        myPost2.style.display = "flex";
        myPost3.style.display = "flex";
        myPost4.style.display = "flex";
        mybookmarked1.style.display = "none";
        mybookmarked2.style.display = "none";
        mybookmarked3.style.display = "none";
        mybookmarked4.style.display = "none";
        postsAll.style.display = "none";
        postsCommunity.style.display = "none";
        postsRecipe.style.display = "none";
        postsInterior.style.display = "none";
        bookmarksAll.style.display = "none";
        bookmarksCommunity.style.display = "none";
        bookmarksRecipe.style.display = "none";
        bookmarksInterior.style.display = "none";
        mypageAllPost.style.display = "none";
        myPosts.style.color='black';
        bookmarked.style.color='var(--dark--gray--color)';
        myPost1.style.color='var(--dark--gray--color)';
        myPost2.style.color='var(--dark--gray--color)';
        myPost3.style.color='var(--dark--gray--color)';
        myPost4.style.color='var(--dark--gray--color)';
        gridIcon.src="/static/img/grid.svg"
        bookmarkIcon.src="/static/img/bookmark.svg"


        myPost1.addEventListener("click", function() {
            postsAll.style.display = "flex";
            postsInterior.style.display = "none";
            postsRecipe.style.display = "none";
            postsCommunity.style.display = "none";
            mypageAllPost.style.display = "flex";
            myPost1.style.color='black';
            myPost2.style.color='var(--dark--gray--color)';
            myPost3.style.color='var(--dark--gray--color)';
            myPost4.style.color='var(--dark--gray--color)';
        });
        myPost2.addEventListener("click", function() {
            postsAll.style.display = "none";
            postsInterior.style.display = "flex";
            postsRecipe.style.display = "none";
            postsCommunity.style.display = "none";
            mypageAllPost.style.display = "flex";
            myPost1.style.color='var(--dark--gray--color)';
            myPost2.style.color='black';
            myPost3.style.color='var(--dark--gray--color)';
            myPost4.style.color='var(--dark--gray--color)';
        });
        myPost3.addEventListener("click", function() {
            postsAll.style.display = "none";
            postsInterior.style.display = "none";
            postsRecipe.style.display = "flex";
            postsCommunity.style.display = "none";
            mypageAllPost.style.display = "flex";
            myPost1.style.color='var(--dark--gray--color)';
            myPost2.style.color='var(--dark--gray--color)';
            myPost3.style.color='black';
            myPost4.style.color='var(--dark--gray--color)';
        });
        myPost4.addEventListener("click", function() {
            postsAll.style.display = "none";
            postsInterior.style.display = "none";
            postsRecipe.style.display = "none";
            postsCommunity.style.display = "flex";
            mypageAllPost.style.display = "flex";
            myPost1.style.color='var(--dark--gray--color)';
            myPost2.style.color='var(--dark--gray--color)';
            myPost3.style.color='var(--dark--gray--color)';
            myPost4.style.color='black';
        });
    });



    // 북마크 한 글
    bookmarked.addEventListener("click", function() {
        subCategoryPost.style.display = "none";
        subCategoryookmark.style.display = "flex";
        myPost1.style.display = "none";
        myPost2.style.display = "none";
        myPost3.style.display = "none";
        myPost4.style.display = "none";
        mybookmarked1.style.display = "flex";
        mybookmarked2.style.display = "flex";
        mybookmarked3.style.display = "flex";
        mybookmarked4.style.display = "flex";
        postsAll.style.display = "none";
        postsCommunity.style.display = "none";
        postsRecipe.style.display = "none";
        postsInterior.style.display = "none";
        bookmarksAll.style.display = "none";
        bookmarksCommunity.style.display = "none";
        bookmarksRecipe.style.display = "none";
        bookmarksInterior.style.display = "none";
        mypageAllPost.style.display = "none";
        myPosts.style.color='var(--dark--gray--color)';
        bookmarked.style.color='black';
        mybookmarked1.style.color='var(--dark--gray--color)';
        mybookmarked2.style.color='var(--dark--gray--color)';
        mybookmarked3.style.color='var(--dark--gray--color)';
        mybookmarked4.style.color='var(--dark--gray--color)';
        gridIcon.src="/static/img/grid-gray.svg"
        bookmarkIcon.src="/static/img/bookmark-black.svg"
        

        mybookmarked1.addEventListener("click", function() {
            bookmarksAll.style.display = "flex";
            bookmarksInterior.style.display = "none";
            bookmarksRecipe.style.display = "none";
            bookmarksCommunity.style.display = "none";
            mypageAllPost.style.display = "flex";
            mybookmarked1.style.color='black';
            mybookmarked2.style.color='var(--dark--gray--color)';
            mybookmarked3.style.color='var(--dark--gray--color)';
            mybookmarked4.style.color='var(--dark--gray--color)';
        });
        mybookmarked2.addEventListener("click", function() {
            bookmarksAll.style.display = "none";
            bookmarksInterior.style.display = "flex";
            bookmarksRecipe.style.display = "none";
            bookmarksCommunity.style.display = "none";
            mypageAllPost.style.display = "flex";
            mybookmarked1.style.color='var(--dark--gray--color)';
            mybookmarked2.style.color='black';
            mybookmarked3.style.color='var(--dark--gray--color)';
            mybookmarked4.style.color='var(--dark--gray--color)';
        });
        mybookmarked3.addEventListener("click", function() {
            bookmarksAll.style.display = "none";
            bookmarksInterior.style.display = "none";
            bookmarksRecipe.style.display = "flex";
            bookmarksCommunity.style.display = "none";
            mypageAllPost.style.display = "flex";
            mybookmarked1.style.color='var(--dark--gray--color)';
            mybookmarked2.style.color='var(--dark--gray--color)';
            mybookmarked3.style.color='black';
            mybookmarked4.style.color='var(--dark--gray--color)';
        });
        mybookmarked4.addEventListener("click", function() {
            bookmarksAll.style.display = "none";
            bookmarksInterior.style.display = "none";
            bookmarksRecipe.style.display = "none";
            bookmarksCommunity.style.display = "flex";
            mypageAllPost.style.display = "flex";
            mybookmarked1.style.color='var(--dark--gray--color)';
            mybookmarked2.style.color='var(--dark--gray--color)';
            mybookmarked3.style.color='var(--dark--gray--color)';
            mybookmarked4.style.color='black';
        });
    });

    //팝업창
    // document.getElementById('profile-edit-btn').addEventListener('click', function(event) {
    //     event.preventDefault();
    //     document.getElementById('profile-edit-popup').style.display = 'block';
    // });

    // document.getElementById('profile-edit-form').addEventListener('submit', function() {
    //     document.getElementById('profile-edit-popup').style.display = 'none';
    // });

    // document.getElementById('password-change-btn').addEventListener('click', function(event) {
    //     event.preventDefault();
    //     document.getElementById('profile-edit-popup').style.display = 'none';
    //     document.getElementById('password-change-popup').style.display = 'block';
    // });

    // document.getElementById('password-change-form').addEventListener('submit', function() {
    //     document.getElementById('password-change-popup').style.display = 'none';

    // });

    // 프로필 편집 팝업 열기
    document.getElementById('profile-edit-btn').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('profile-edit-popup').style.display = 'block';
    });

    // 프로필 편집 폼 제출
    document.getElementById('profile-edit-form').addEventListener('submit', function(event) {
        event.preventDefault();
        fetch(this.action, {
            method: 'POST',
            body: new FormData(this),
        }).then(response => response.json()).then(data => {
            if (data.status === 'success') {
                location.reload(); // 페이지를 새로고침하여 변경사항을 반영합니다.
            } else {
                console.error('Form submission error:', data.errors);
                document.getElementById('profile-edit-popup').style.display = 'block'; // 오류가 있을 경우 팝업을 다시 엽니다.
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    });

    // 비밀번호 변경 팝업 열기
    document.getElementById('password-change-btn').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('profile-edit-popup').style.display = 'none';
        document.getElementById('password-change-popup').style.display = 'block';
    });

    // 비밀번호 변경 팝업 폼 제출
    document.getElementById('password-change-form').addEventListener('submit', function() {
        // 폼 제출 후 팝업 닫기
        document.getElementById('password-change-popup').style.display = 'none';
    });

})