using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;

public class CapsuleTest : MonoBehaviour
{

    Vector3 rotationValue;

    // Start is called before the first frame update
    void Start()
    {
        rotationValue = new Vector3(0f, 1f, 0f);
    }

    // Update is called once per frame
    void Update()
    {
        this.transform.Rotate(rotationValue);
    }
}
