class Playlist extends React.Component {
    render() {

        const songNames = this.props.tracks.map(track => (
            <Song key={track.url}
            updateTrack = {this.props.updateTrack}
            songPlaying = {this.props.trackPlaying}
            uri={track.uri} 
            track={track.name} />
        ));


        return (
            <div>
                <ul className="playlist-panel">
                    <span> {songNames} </span>
                </ul>
            </div>
        );
    }
}