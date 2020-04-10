import * as React from "react";
import { ActivityIndicator, StyleSheet } from "react-native";
import { Image } from "react-native-elements";
export default function OneImage(props) {
  return (
    <Image
      source={props.source}
      style={{ width: 200, height: 300 }}
      PlaceholderContent={<ActivityIndicator />}
      containerStyle={styles.image}
    />
  );
}
const styles = StyleSheet.create({
  image: { borderRadius: 20, overflow: "hidden", marginBottom: 20 },
});
