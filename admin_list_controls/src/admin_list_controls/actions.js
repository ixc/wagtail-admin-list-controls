import * as constants from "./constants";

export function create_action(action) {
    switch(action.action_type) {
        case 'toggle_panel':
            return {
                type: constants.TOGGLE_PANEL,
                ref: action.ref,
            };
        case 'close_panel':
            return {
                type: constants.CLOSE_PANEL,
                ref: action.ref,
            };
        case 'set_value':
            return {
                type: constants.SET_VALUE,
                name: action.name,
                value: action.value,
            }
        case 'remove_value':
            return {
                type: constants.REMOVE_VALUE,
                name: action.name,
                value: action.value,
            }
        case 'submit_form':
            return {
                type: constants.SUBMIT_FORM,
            };
        case 'append_value':
        case 'link':
        default:
            console.error('Unknown action type', action);
            throw new Error(`Unknown action ${action.action_type}`);
    }
}