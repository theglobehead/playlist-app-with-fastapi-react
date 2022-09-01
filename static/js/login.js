$(() => {
    let username = Cookies.get('username')

    if(username){
        $("#username_input:first").val(username)
    }
})