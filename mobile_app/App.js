import * as React from "react";
import { Button, View, Text } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import ReportScreen from "./Screens/ReportScreen";
import InputImage from "./Screens/InputImage";
import Recommendation from "./Screens/Recommendation";
import Questionnaire from "./Screens/QuestionnaireScreen";
import LandingScreen from "./Screens/LandingScreen";
import ConfirmImage from "./Screens/ConfirmImage";
import LoadingScreen from "./Screens/LoadingScreen";

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen
          name="Home"
          component={LandingScreen}
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen
          name="Questionnaire"
          component={Questionnaire}
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen
          name="Take Image"
          component={InputImage}
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen name="Confirm Selfie" component={ConfirmImage} />
        <Stack.Screen
          name="Fetch Report"
          component={LoadingScreen}
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen
          name="Report"
          component={ReportScreen}
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen
          name="Products Recommendation"
          component={Recommendation}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
