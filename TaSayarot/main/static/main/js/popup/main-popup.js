const uploadPopup = document.getElementById("upload-screen");
            
function openUploadPopup(){
    uploadPopup.showModal();
}
            
function closeUploadPopup(){
    uploadPopup.close();
}
            
const postPopup = document.getElementById("post-screen");
            
function openPostPopup(name, date, id, text, likes, file, profile_image, type, comments){
    const my_file = document.getElementById("post-photo");
    const my_name = document.getElementById("name");
    const my_date = document.getElementById("date");
    const my_id = document.getElementById("id");
    const my_text = document.getElementById("text");
    const my_likes = document.getElementById("like_amount");
    const my_image = document.getElementById("profile-pic");

    //likes
    const my_like_btn = document.getElementById("like-btn");

    //comments
    const my_comment_btn = document.getElementById("comment-btn");
    const comment_section = document.getElementById("other-comments");

    my_name.innerHTML = name;
    my_date.innerHTML = date;
    my_id.innerHTML = "מס' פוסט: " + id;
    my_text.innerHTML = text;
    my_likes.innerHTML = likes;
    my_image.src = profile_image;

    // handles if mp4 file or not, creates a tag accordingly
    if (type == "mp4") {
        my_file.innerHTML = "<video controls style='max-width: 125%; height: auto; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 100%; max-height: 100%;' src='" + file + "' id='post-video'><source type='video/mp4'>Your browser does not support the video tag.</video>";
    }
    else {
        my_file.innerHTML = "<img src='" + file + "' style='max-width: 125%; height: auto; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 100%; max-height: 100%;'>";
    }

    //sets the value of the like btn so that I can get it from the server
    my_like_btn.setAttribute("value", id);

    //sets the value of the comment btn so that I can get it from the server
    my_comment_btn.setAttribute("value", id);

    comment_section.innerHTML = "";
    for (let i = 0; i < comments.length; i++) {
        comment_section.innerHTML += "<div class='some-comment'><img src='" + comments[i][0] + "' class='profile-pic'><p class='comment'>" + comments[i][1] + "</p></div>";
    }

    postPopup.showModal();
}
            
function closePostPopup(){
    postPopup.close();
}

function lol() {
    console.log("Hello world");
}