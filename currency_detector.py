import cv2
import numpy as np
import os

class CurrencyDetector:
    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=1000)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.reference_data = {}
        self.load_reference_images()

    def load_reference_images(self):
        reference_dir = "reference_notes"
        if not os.path.exists(reference_dir):
            os.makedirs(reference_dir)
            print(f"Please add reference currency images in {reference_dir} folder")
            return

        for filename in os.listdir(reference_dir):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                try:
                    denomination = os.path.splitext(filename)[0]
                    img_path = os.path.join(reference_dir, filename)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

                    if img is not None:
                        kp, des = self.orb.detectAndCompute(img, None)
                        self.reference_data[denomination] = {
                            'image': img,
                            'keypoints': kp,
                            'descriptors': des
                        }
                    else:
                        print(f"Warning: Could not read image {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

    def verify_currency(self, test_img_path, threshold=30):
        try:
            if not os.path.exists(test_img_path):
                return "Error: Test image not found."

            test_img = cv2.imread(test_img_path)
            if test_img is None:
                return "Error: Could not read test image."

            test_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
            test_kp, test_des = self.orb.detectAndCompute(test_gray, None)

            if test_des is None:
                return "Error: Could not extract features from test image."

            best_match = None
            best_score = 0
            best_denomination = None

            for denomination, ref_data in self.reference_data.items():
                ref_des = ref_data['descriptors']
                matches = self.bf.match(test_des, ref_des) if (test_des is not None and ref_des is not None) else []
                match_score = len(matches)

                if match_score > best_score:
                    best_score = match_score
                    best_denomination = denomination
                    best_match = {
                        'matches': matches,
                        'ref_img': ref_data['image'],
                        'ref_kp': ref_data['keypoints'],
                        'test_img': test_gray,
                        'test_kp': test_kp
                    }

            is_genuine = best_score >= threshold
            result = {
                'is_genuine': is_genuine,
                'denomination': best_denomination,
                'match_score': best_score,
                'match_data': best_match,
                'test_image': test_img
            }

            return result

        except Exception as e:
            return f"Error during verification: {str(e)}"