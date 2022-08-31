function checkArtistExists(url, $artistInput, $createArtistBtn=null){
    if($artistInput.val() === ""){
        $artistInput.removeClass("input-invalid")
        return true;
    }

    let result = false

    let formData = new FormData();
    formData.append('artist_name', $artistInput.val())

    $.ajax({
        url: url,
        data: formData,
        type: 'POST',
        contentType: false,
        processData: false,
        async: false,
        success: (data) => {
            if(data["result"]){
                $artistInput.removeClass("input-invalid")
                if($createArtistBtn){
                    $createArtistBtn.prop("disabled", false)
                }
                result = true
            }else{
                $artistInput.addClass("input-invalid")
                if($createArtistBtn){
                    $createArtistBtn.prop("disabled", true)
                }
            }
        }
    });

    return result
}
