let curAudioNum = null
let curAudioPaused = false

function switchAudio(audioNum){
    if(curAudioNum){
        pauseAudio(curAudioNum)
        $(`#audio-${ curAudioNum }:first`)[0].currentTime = 0
    }
    $(`#audio-${ audioNum }:first`)[0].play()
    $(`#audio-${ audioNum }:first`).parent().addClass("selected")
    curAudioNum = audioNum
}

function pauseAudio(audioNum){
    $(`#audio-${ audioNum }:first`)[0].pause()
    $(`#audio-${ audioNum }:first`).parent().removeClass("selected")
}

function playAudio(audioNum){
    $(`#audio-${ audioNum }:first`)[0].play()
    $(`#audio-${ audioNum }:first`).parent().addClass("selected")
}

function toggleAudio(audioNum){
    if(curAudioNum == audioNum){
        if(curAudioPaused){
            playAudio(audioNum)
        }else{
            pauseAudio(audioNum)
        }
        curAudioPaused = !curAudioPaused
    }else{
        switchAudio(audioNum)
    }
}