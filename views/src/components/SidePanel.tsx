import React from 'react';
import i18n from 'i18next';
import Cookies from "universal-cookie";

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
                <a className={"btn-leaf"} href={"#"}>{ i18n.t("strings.playlists") as string }</a>
                <a className={"btn-leaf"} href={"#"}>{ i18n.t("strings.settings") as string }</a>
                <a className={"btn-leaf"} href={"#"}>{ i18n.t("strings.discover") as string }</a>
                <a className={"btn-leaf"} href={"#"}>{ i18n.t("strings.artists") as string }</a>
            </div>
            <a className={"log-out-btn"} onClick={() => logUserOut()}>{ i18n.t("strings.log_out") as string }</a>
        </div>
    );
}

export default SidePanel;