import counterReducer from './counter';
import reducer from './switch';
import {combineReducers} from 'redux'; 

// line 1 of this page brings in counterReducers from the file counter
// so if there were any more reducers we would bring those in and combing them in this format

const allReducers = combineReducers({
    counterReducer,
    reducer
});

export default allReducers; //-> export this object so the store as access to it
