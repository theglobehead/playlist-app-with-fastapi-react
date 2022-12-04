import SidePanel from "../components/side_panel";
import React, { Component } from 'react';
import i18n from 'i18next';
import axios from "axios";
import Cookies from 'universal-cookie';
import {Simulate} from "react-dom/test-utils";
import playing = Simulate.playing;

const cookies = new Cookies();

type Playlist = {
    "playlist_uuid": string,
    "playlist_name": string,
    "modified": string,
    "created": string,
    "is_deleted": boolean,
  }

export class YourPlaylists extends Component {
    openModal(modalName: string){

    }

    closeModal(modalName: string){

    }

    getUserPlaylists(){
        let result: any[] = []

        const formData = new FormData();
        formData.append("user_uuid", cookies.get("user_uuid"))

        axios.post("http://127.0.0.1:8000/get_user_playlists", formData)
        .then(function (response){
            for(let i in response.data.user_playlists){
                let playlist = response.data.user_playlists[i]
                result.push(playlist)
            }
        })
        .catch(function (error) {
            console.error(error);
        });

        console.log(typeof result)
        console.log(result)

        return result
    }

    render() {
        return (
            <div>
                <SidePanel></SidePanel>
                <div style={{width: "80%", marginLeft: "auto", boxSizing: "border-box", padding: "5vh 5% 5vh 5%"}}>
                    <button
                        style={{width: "fit-content"}}
                        className={"btn-rounded"}
                        onClick={() => this.openModal('create_playlist_modal')}
                    >
                        { i18n.t('strings.create_new') as string } +
                    </button>
                    { /* Using tables for learning */ }
                    <table className={"playlist-rows"}>
                        {
                            this.getUserPlaylists().map((a) => {
                               return <li>aaaaaa</li>;
                            })
                        }

                      {/*
                      {% for playlist in playlists %}
                      <tr className="playlist-row-tr">
                        <td>
                          <table className="playlist-box shadow">
                            <tr>
                              <td className="image-td">
                                <img
                                    src="{{ url_for(" site.get_profile_pic", user_uuid=user.user_uuid) }}"
                                    className="shadow"
                                    style="width: 10vw; height: 10vw;"
                                >
                              </td>
                              <td className="info-td">
                                <h3>{{playlist.playlist_name}}</h3>
                                <p>{{_('strings.songs')}}: {{playlist.songs | length}}</p>
                              </td>
                              <td className="btn-td">
                                <a
                                    style="margin-top: 15px; border-radius: 20% 0 0 20%; border-width: 2px 0px 2px 2px;"
                                    className="btn-scifi"
                                    type="submit"
                                    href="{{ url_for(" playlists.playlist_page", playlist_uuid=playlist.playlist_uuid) }}"
                                >{{_('strings.open')}}</a>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                      {% endfor %}
                      */}
                    </table>
                </div>

                <div className={"modal-wrapper modal-closed"} id={"create_playlist_modal"}>
                    <form
                        className="rounded-form form-toggleable shadow"
                        action=""
                        method="post" style={{
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            height: "fit-content",
                            width: "20%"
                        }}
                    >
                        <input type="hidden" name="owner_user_uuid" value="{{ user.user_uuid }}"/>
                        <a
                            className="toggle-x"
                            onClick={ () => this.closeModal('create_playlist_modal') }
                        >x</a>
                        <h3 style={{textAlign: "center"}}>
                            { i18n.t('strings.new_playlist') as string }:
                        </h3>
                        <div style={{width: "80%"}}>
                            <p style={{marginTop: "15px"}}>
                                { i18n.t('strings.name_playlist') as string }:
                            </p>
                            <input placeholder="Name" name="playlist_name" required autoComplete="off"/>
                        </div>
                        <button
                            style={{marginTop: "15px", borderRadius: "20% 20% 0 0"}}
                            className="btn-scifi"
                            type="submit"
                        >{ i18n.t('strings.create') as string }</button>
                    </form>
                </div>
            </div>
        );
    }
}
