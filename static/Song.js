class Song extends React.Component {

    selectSong = (e) => {
        this.props.updateTrack(e.target.value);
    }

    render() {
        return (
            <button
                value={this.props.uri}
                onClick ={this.selectSong}> {this.props.track}
            </button>
        );
    }
}