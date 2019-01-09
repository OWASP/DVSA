export default (state = {}, action) => {

    switch(action.type) {
        case 'LOGIN':
            return {
                uid: action.user.uid,
                name: action.user.displayName,
                email: action.user.email !== null ? action.user.email : action.user.providerData[0].email,
                image: action.user.photoURL,
                fid: action.user.providerData[0].uid
            };
        case 'LOGOUT':
            return {};
        default:
            return state;
    }
};