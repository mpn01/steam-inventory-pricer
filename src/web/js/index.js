const total_value = document.querySelector("#total-value");
const updateButton = document.querySelector("#bttn");

updateButton.addEventListener("click", () => {
    eel.getSkinPrices()(function(ret) {
        total_value.innerHTML = ret[1];
    })
})