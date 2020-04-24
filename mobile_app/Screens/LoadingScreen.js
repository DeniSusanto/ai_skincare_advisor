import * as React from "react";
import { View, Text, ActivityIndicator, StyleSheet } from "react-native";
import { Divider, Image, Tooltip, Icon } from "react-native-elements";
import Color from "../Cons/Color";
import Api from "../Cons/Api";
export default function LoadingScreen(props) {
  processReport(props);
  async function processReport() {
    let image_64 = props.route.params.image_64;
    let questionnaire = props.route.params.questionnaire;
    let formData = new FormData();
    formData.append("image", image_64);
    formData.append("questionnaire", JSON.stringify(questionnaire));

    await fetch(Api.api_link, {
      method: "POST",
      headers: {
        "Content-Type": "multipart/form-data",
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        let content = data.body;
        props_data = {
          content: content,
        };
        props.navigation.navigate("Report", props_data);
      })
      .catch((error) => {
        console.error(error);
      });
  }
  return (
    <View
      style={{
        justifyContent: "center",
        alignItems: "center",
        width: "100%",
        height: "100%",
        backgroundColor: "#e5eff1",
      }}
    >
      <Image
        source={require("../assets/images/loading.gif")}
        style={{ width: 300, height: 300 }}
        PlaceholderContent={<ActivityIndicator />}
      />
      <Text style={{ fontStyle: "italic", fontSize: 14 }}>
        Analyzing Your Facial Features
      </Text>
    </View>
  );
}
