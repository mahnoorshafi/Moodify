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
                <h1> Playlist: {this.props.name} </h1>
                    <ul className="playlist">
                        <span> {songNames} </span>
                    </ul>
            </div>
        );
    }
}