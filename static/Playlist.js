class Playlist extends React.Component {
    render() {

        const songNames = this.props.tracks.map(track => (
            <Song
            updateTrack = {this.props.updateTrack}
            songPlaying = {this.props.trackPlaying} 
            track={track} />
        ));

        return (
            <div> 
                {songNames}
            </div>
        )
    }
}