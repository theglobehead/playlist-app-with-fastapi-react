function closeModal(modalId){
    $(`#${ modalId }`).css("display", "none")
}

function openModal(modalId){
    $(`#${ modalId }`).css("display", "flex")
}