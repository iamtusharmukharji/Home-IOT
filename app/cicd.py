from app import app
import git

@app.route('/trigger/cicd',methods=['POST'])
def cicd_trigger():
    repo = git.Repo('./Home-IOT')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200
