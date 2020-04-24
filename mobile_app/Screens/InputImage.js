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

export default class InputImage extends React.Component {
  questionnaireProps = this.props.route.params;
  componentDidMount() {
    this.getPermissionAsync();
  }

  getPermissionAsync = async () => {
    const per1 = await Permissions.askAsync(Permissions.CAMERA_ROLL);
    if (per1["status"] !== "granted") {
      alert("Sorry, we need media permissions to continue!");
    }
    const per2 = await Permissions.askAsync(Permissions.CAMERA);
    if (per2["status"] !== "granted") {
      alert("Sorry, we need camera permissions to continue!");
    }
  };

  _getImage = async (mode) => {
    try {
      let launch = ImagePicker.launchCameraAsync;
      if (mode == "roll") {
        launch = ImagePicker.launchImageLibraryAsync;
      }
      let result = await launch({
        base64: true,
        allowsEditing: true,
        aspect: [2, 3],
        quality: 1,
      });
      if (!result.cancelled) {
        this.setState({ image: result.base64 });
        let confirmationParams = {
          questionnaire: this.questionnaireProps,
          image: result.uri,
          image_64: result.base64,
        };
        this.props.navigation.navigate("Confirm Selfie", confirmationParams);
      }
    } catch (E) {
      console.log(E);
    }
  };

  state = {
    image: null,
  };
  styles = StyleSheet.create({
    overlay: {
      backgroundColor: Color.primary_overlay,
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
    },
  });
  render() {
    let { image } = this.state;

    return (
      <View style={{ width: "100%", height: "100%" }}>
        <View style={{ width: "100%", height: "100%", position: "absolute" }}>
          <Image
            source={require("../assets/images/landing_bg.jpg")}
            style={{ width: "100%", height: "100%" }}
            resizeMode="cover"
          />
          <View style={this.styles.overlay} />
        </View>
        <Header
          statusBarProps={{ translucent: true }}
          centerComponent={{
            text: "Take Image",
            style: { color: "#fff", fontSize: 22, fontWeight: "bold" },
          }}
          backgroundColor={Color.primary}
        />
        <View
          style={{
            width: "100%",
            height: "80%",
            justifyContent: "space-evenly",
            alignItems: "center",
          }}
        >
          <TouchableOpacity
            style={{
              width: "60%",
              justifyContent: "center",
              alignItems: "center",
            }}
            onPress={() => {
              this._getImage("roll");
            }}
          >
            <View
              style={{
                width: "100%",
                height: 200,
                paddingVertical: 10,
                paddingHorizontal: 10,
                justifyContent: "space-evenly",
                alignItems: "center",
                backgroundColor: Color.white_overlay,
                borderRadius: 20,
              }}
            >
              <Icon name="perm-media" size={80} />
              <Text style={{ fontSize: 16 }}>Pick image from phone</Text>
            </View>
          </TouchableOpacity>
          <TouchableOpacity
            style={{
              width: "60%",
              justifyContent: "center",
              alignItems: "center",
            }}
            onPress={() => {
              this._getImage("cam");
            }}
          >
            <View
              style={{
                width: "100%",
                height: 200,
                paddingVertical: 10,
                paddingHorizontal: 10,
                justifyContent: "space-evenly",
                alignItems: "center",
                backgroundColor: Color.white_overlay,
                borderRadius: 20,
              }}
            >
              <Icon name="photo-camera" size={80} />
              <Text style={{ fontSize: 16 }}>Take image from camera</Text>
            </View>
          </TouchableOpacity>
        </View>
      </View>
    );
  }
}
