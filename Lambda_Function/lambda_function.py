### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_slots(intent_request)["firstName"]
    age = int(get_slots(intent_request)["age"])
    investment_amount = int(get_slots(intent_request)["investmentAmount"])
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]


    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        ### YOUR DATA VALIDATION CODE STARTS HERE ###

        ### YOUR DATA VALIDATION CODE ENDS HERE ###

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation

    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE STARTS HERE ###\
    if investment_amount > 4999:
        if age > 0 and age < 65:
            if risk_level == "None":
                final_recommendation = f"${investment_amount*1} bonds (AGG), $0 equities (SPY)"
            elif risk_level == "Very Low":
                final_recommendation = f"${investment_amount*0.8} bonds (AGG), ${investment_amount*0.2} equities (SPY)"
            elif risk_level == "Low":
                final_recommendation = f"${investment_amount*0.6} bonds (AGG), ${investment_amount*0.4} equities (SPY)"
            elif risk_level == "Medium":
                final_recommendation = f"${investment_amount*0.4} bonds (AGG), ${investment_amount*0.6} equities (SPY)"
            elif risk_level == "High":
                final_recommendation = f"${investment_amount*0.2} bonds (AGG), ${investment_amount*0.8} equities (SPY)"
            elif risk_level == "Very High":
                final_recommendation = f"$0 bonds (AGG), ${investment_amount*1} equities (SPY)"
            else:
                final_recommendation = "No risk selection, select again."
        else:
            final_recommendation = "You can't invest as you're too old or have a negative age (which is not possible), please try again."
    else: 
        final_recommendation = "Your investment needs to be equal to 5000 or more."
    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE ENDS HERE ###

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": final_recommendation
        },
    )


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "BookCar":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
