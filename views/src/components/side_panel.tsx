import React from 'react';
import Cookies from 'universal-cookie';

function SidePanel() {
    const cookies = new Cookies();

    const logUserOut = () => {
        cookies.set("user_uuid", "")
        cookies.set("token_uuid", "")
        window.location.reload();
    }

    return (
        <div className={"side-panel"}>
            <div className={"side-panel-head"}>
                <img
                    src={"https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg"}
                    className={"shadow side-panel-img"}
                />
                <p className={"side-panel-user-name"}>
                    placeholder name
                </p>
            </div>
            <div className={"side-panel-buttons"}>
                <a className={"btn-leaf"} href={"#"}>playlists</a>
                <a className={"btn-leaf"} href={"#"}>settings</a>
                <a className={"btn-leaf"} href={"#"}>discover</a>
                <a className={"btn-leaf"} href={"#"}>artists</a>
            </div>
            <a className={"log-out-btn"} onClick={() => logUserOut()}>Log out</a>
        </div>
    );
}

export default SidePanel;