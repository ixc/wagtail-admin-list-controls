import {SET_VALUE, SUBMIT_FORM, TOGGLE_PANEL, REMOVE_VALUE} from "./constants";

export function create_action(action) {
    switch(action.action_type) {
        case 'toggle_panel':
            return {
                type: TOGGLE_PANEL,
                ref: action.ref,
            };
        case 'set_value':
            return {
                type: SET_VALUE,
                name: action.name,
                value: action.value,
            }
        case 'remove_value':
            return {
                type: REMOVE_VALUE,
                name: action.name,
                value: action.value,
            }
        case 'submit_form':
            return {
                type: SUBMIT_FORM,
            };
        case 'append_value':
        case 'link':
        default:
            console.error('Unknown action type', action);
            throw new Error(`Unknown action ${action.action_type}`);
    }
}