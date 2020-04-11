import * as React from "react";
import { View, StyleSheet, Text, ActivityIndicator } from "react-native";
import { Image, Icon, Input, Button, Divider } from "react-native-elements";
import Color from "../Cons/Color";
import { useFonts } from "@use-expo/font";
import { AppLoading } from "expo";

export default function CatalogueList(props) {
  let [fontsLoaded] = useFonts({
    Kaushan: require("../assets/fonts/KaushanScript-Regular.otf"),
  });
  if (!fontsLoaded) {
    return <AppLoading />;
  } else {
    return (
      <View style={{ width: "100%", height: "100%" }}>
        <View style={{ width: "100%", height: "100%", position: "absolute" }}>
          <Image
            source={require("../assets/images/landing_bg_2.jpg")}
            style={{ width: "100%", height: "100%" }}
            resizeMode="cover"
          />
          <View style={styles.overlay} />
        </View>
        <View
          style={{
            width: "100%",
            height: "100%",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <View
            style={{
              width: "90%",
              paddingVertical: 30,
              justifyContent: "flex-start",
              alignItems: "center",
              backgroundColor: Color.white_overlay,
              borderRadius: 20,
            }}
          >
            <View
              style={{
                justifyContent: "center",
                alignItems: "center",
                marginBottom: 30,
                width: "100%",
              }}
            >
              <Text style={styles.title}>AI Skincare </Text>
              <Text style={styles.title}>Advisor </Text>
            </View>
            <View
              style={{
                width: "90%",
                justifyContent: "center",
                alignItems: "center",
                marginBottom: 10,
              }}
            >
              <Input
                placeholder="Input Username"
                placeholderTextColor="grey"
                label="Username"
                containerStyle={{
                  marginBottom: 10,
                }}
                labelStyle={{
                  color: "black",
                }}
                inputStyle={{
                  marginLeft: 10,
                }}
                leftIcon={<Icon name="account-circle" size={24} color="grey" />}
              />

              <Input
                placeholder="Input Password"
                placeholderTextColor="grey"
                label="Password"
                labelStyle={{
                  color: "black",
                }}
                containerStyle={{
                  marginBottom: 20,
                }}
                inputStyle={{
                  marginLeft: 10,
                }}
                leftIcon={<Icon name="lock" size={24} color="grey" />}
              />
              <Button
                title="Login"
                buttonStyle={{
                  backgroundColor: Color.darker_primary,
                }}
                containerStyle={{
                  borderRadius: 20,
                  overflow: "hidden",
                  width: "40%",
                }}
              />
            </View>
            <View
              style={{
                width: "70%",
                flexDirection: "row",
                justifyContent: "space-evenly",
                alignItems: "center",
                marginBottom: 10,
              }}
            >
              <Divider style={{ height: 2, width: "40%" }} />
              <Text>OR</Text>
              <Divider style={{ height: 2, width: "40%" }} />
            </View>
            <View
              style={{
                width: "90%",
                justifyContent: "center",
                alignItems: "center",
                marginBottom: 10,
              }}
            >
              <Button
                title="Continue as Guest"
                buttonStyle={{
                  backgroundColor: Color.darker_primary,
                  paddingHorizontal: 20,
                }}
                containerStyle={{
                  borderRadius: 20,
                  overflow: "hidden",
                }}
                onPress={() => props.navigation.navigate("Questionnaire")}
              />
            </View>
          </View>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  overlay: {
    backgroundColor: Color.primary_overlay,
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  title: {
    fontFamily: "Kaushan",
    fontSize: 50,
  },
});
