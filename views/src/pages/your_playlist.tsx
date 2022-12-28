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

type PageState = {
  playlists: any[]
}

export class YourPlaylists extends Component<{}, PageState> {
    openModal(modalName: string){
        console.log("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    }

    closeModal(modalName: string){

    }

    getUserPlaylists(){
        let result: any[] = []
        return result
    }

    render() {
        console.log("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")

        this.setState({"playlists": this.getUserPlaylists()})
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
                            this.getUserPlaylists().map(() => {
                                return <h1>feiieowgwegre</h1>
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
