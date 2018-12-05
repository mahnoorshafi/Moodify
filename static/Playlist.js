class Playlist extends React.Component {
    render() {

        const songNames = this.props.tracks.map(track => (
            <Song
            selectSong = {this.props.selectSong}
            updateTrack = {this.props.updateTrack}
            songPlaying = {this.props.trackPlaying}
            uri={track.uri} 
            track={track.name} />
        ));


        return (
            <div> 
                {songNames}
            </div>
        )
    }
}