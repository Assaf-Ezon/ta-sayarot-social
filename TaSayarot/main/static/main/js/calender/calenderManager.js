//handles the calender
const currentDate = document.querySelector(".current-date");
const dayTag = document.querySelector(".days");
const prevNextIcon = document.querySelectorAll(".icons span");

//handles the value of the "change btn"
const change_btn = document.getElementById("change-btn");

//getting new date, current year and month
let date = new Date();
let currentYear = date.getFullYear();
let currentMonth = date.getMonth();
            
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
            
const renderCalender = () => {     
    let lastDateofMonth = new Date(currentYear, currentMonth + 1, 0).getDate(); //gets the last date of the month
    change_btn.setAttribute("value", date.toLocaleDateString("en-US"));
    let liTag = "";

    for (let i = 1; i <= lastDateofMonth; i++) {
        let isToday = i === date.getDate() ? "active" : "";
        if (isToday) {
            change_btn.setAttribute("value", (currentMonth + 1) + "/" + date.getDate() + "/" + currentYear);
        }
        liTag += "<li class=" + isToday + ">" + i + "</li>";
    }
                
    currentDate.innerHTML = months[currentMonth] + " " + currentYear;
    dayTag.innerHTML = liTag;     
                
    const daysIcon = document.querySelectorAll(".days li");
                
    daysIcon.forEach(icon => {
        icon.addEventListener("click", () => {
            date = new Date(currentYear, currentMonth, icon.textContent);
            renderCalender()
        });
    });
};
            
renderCalender();
            
prevNextIcon.forEach(icon => {
    icon.addEventListener("click", () => {
        currentMonth = icon.id === "prev" ? currentMonth - 1 : currentMonth + 1;

        if (currentMonth < 0 || currentMonth > 11) {
            date = new Date(currentYear, currentMonth, date.getDate());
            currentYear = date.getFullYear();
            currentMonth = date.getMonth();
        }

        renderCalender();
    });
});