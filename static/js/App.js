class App extends React.Component {
        state = {
            trackPlaying: '',
            playlistTracks: []
        }

    componentDidMount () {
        fetch(`/track-info.json`)
        .then(res => res.json())
        .then(data => {
        this.setState({ playlistTracks: data.tracks });
        })
        .catch(err => this.setState({ playlistTracks: "Something went wrong" }));
    }

    updateTrack = (track) => {
        let currentlyPlaying = this.state.trackPlaying;
        if (currentlyPlaying !== track) {
            this.setState({trackPlaying: track});
        }
    }

    nextTrack = () => {
        let currentlyPlaying = this.state.trackPlaying;
        let indexCurrentlyPlaying = this.state.playlistTracks.findIndex(track => {
                return track.uri === currentlyPlaying;
        });
        let nextTrack = this.state.playlistTracks[indexCurrentlyPlaying + 1]
        this.setState({trackPlaying: nextTrack.uri})
    }

    previousTrack = () => {
        let currentlyPlaying = this.state.trackPlaying;
        let indexCurrentlyPlaying = this.state.playlistTracks.findIndex(track => {
                return track.uri === currentlyPlaying;
        });
        let nextTrack = this.state.playlistTracks[indexCurrentlyPlaying - 1]
        this.setState({trackPlaying: nextTrack.uri})
    }

    render() {
        return (
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-6">
                        <Player
                        accessToken={this.props.token}
                        songToPlay={this.state.trackPlaying}
                        nextSong={this.nextTrack}
                        previousSong={this.previousTrack}
                        tracks={this.props.playlistTracks} />
                    </div>
                    <div className="col-sm-6">
                        <Playlist
                        updateTrack={this.updateTrack}
                        songPlaying={this.state.trackPlaying} 
                        tracks={this.state.playlistTracks}
                        name={this.props.name} />
                    </div>
                </div>
            </div>
        )
    };
}