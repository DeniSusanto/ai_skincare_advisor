import * as React from "react";
import { Button, View, Text } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import ReportScreen from "./Screens/ReportScreen";
import InputImage from "./Screens/InputImage";
import Recommendation from "./Screens/Recommendation";

function SelfieImage({ navigation }) {
  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <Text>Pick Picture</Text>
      <Button
        title="Take picture"
        onPress={() => navigation.navigate("Take Image")}
      />
      <Button title="Report" onPress={() => navigation.navigate("Report")} />
    </View>
  );
}

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Selfie Image" component={SelfieImage} />
        <Stack.Screen name="Take Image" component={InputImage} />
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
