let curAudioNum = null
let curAudioPaused = false

function switchAudio(audioNum){
    let $audio_row = $(`#audio-${ audioNum }:first`)
    if(curAudioNum){
        pauseAudio(curAudioNum)
        $(`#audio-${ curAudioNum }:first`)[0].currentTime = 0
    }
    $audio_row[0].play()
    $audio_row.parent().addClass("selected")
    curAudioNum = audioNum
}

function pauseAudio(audioNum){
    let $audio_row = $(`#audio-${ audioNum }:first`)
    $audio_row[0].pause()
    $audio_row.parent().removeClass("selected")
}

function playAudio(audioNum){
    let $audio_row = $(`#audio-${ audioNum }:first`)
    $audio_row[0].play()
    $audio_row.parent().addClass("selected")
}

function toggleAudio(audioNum){
    if(curAudioNum === audioNum){
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
