class App extends React.Component {
        state = {
            trackPlaying: '',
            playlistTracks: []
        }

    updateTrack = (track) => {
        let currentlyPlaying = this.state.trackPlaying;
        if (currentlyPlaying !== track) {
            this.setState({trackPlaying: track});
        }
    }

    nextTrack = () => {
        let currentlyPlaying = this.state.trackPlaying;
        let indexCurrentlyPlaying = this.props.tracks.indexOf(currentlyPlaying)
        let nextTrack = this.props.tracks[indexCurrentlyPlaying + 1]
        this.setState({trackPlaying: nextTrack})
    }

    previousTrack = () => {
        let currentlyPlaying = this.state.trackPlaying;
        let indexCurrentlyPlaying = this.props.tracks.indexOf(currentlyPlaying)
        let previousTrack = this.props.tracks[indexCurrentlyPlaying - 1]
        this.setState({trackPlaying: previousTrack})
    }

    render() {
        return (
            <div>
                <Player
                accessToken={this.props.token}
                songToPlay={this.state.trackPlaying}
                nextSong={this.nextTrack}
                previousSong={this.previousTrack}
                tracks={this.props.tracks} />

                <Playlist
                updateTrack={this.updateTrack}
                songPlaying={this.state.trackPlaying} 
                tracks={this.props.tracks} />
            </div>
        )
    }
}