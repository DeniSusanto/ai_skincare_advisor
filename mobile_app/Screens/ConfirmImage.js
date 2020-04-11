import * as React from "react";
import {
  View,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import * as Permissions from "expo-permissions";
import {
  Button,
  Image,
  Text,
  Input,
  Icon,
  Divider,
  Header,
} from "react-native-elements";
import Color from "../Cons/Color";
export default function ConfirmImage(routeProps) {
  let props = routeProps.route.params;
  const selfieImage = props.image;
  return (
    <View style={{ width: "100%", height: "100%" }}>
      <View style={{ width: "100%", height: "100%", position: "absolute" }}>
        <Image
          source={require("../assets/images/landing_bg.jpg")}
          style={{ width: "100%", height: "100%" }}
          resizeMode="cover"
        />
        <View style={styles.overlay} />
      </View>
      <View
        style={{
          width: "100%",
          justifyContent: "flex-start",
          alignItems: "center",
          paddingVertical: 30,
        }}
      >
        <View style={{ marginBottom: 30 }}>
          <Image
            source={{ uri: selfieImage }}
            style={{ width: 280, height: 420 }}
            PlaceholderContent={<ActivityIndicator />}
            containerStyle={styles.image}
          />
        </View>
        <View
          style={{
            width: "90%",
            flexDirection: "row",
            justifyContent: "space-evenly",
          }}
        >
          <Button
            title="Retake"
            icon={<Icon name="keyboard-backspace" size={24} color="white" />}
            buttonStyle={{
              backgroundColor: "grey",
              paddingHorizontal: 20,
              paddingVertical: 20,
            }}
            containerStyle={{
              borderRadius: 20,
              overflow: "hidden",
            }}
            onPress={() => routeProps.navigation.goBack()}
          />
          <Button
            title="Confirm"
            icon={<Icon name="done" size={24} color="white" />}
            buttonStyle={{
              backgroundColor: "green",
              paddingHorizontal: 20,
              paddingVertical: 20,
            }}
            containerStyle={{
              borderRadius: 20,
              overflow: "hidden",
            }}
            onPress={() => routeProps.navigation.navigate("Report")}
          />
        </View>
      </View>
    </View>
  );
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
  image: { borderRadius: 20, overflow: "hidden", marginBottom: 20 },
});
